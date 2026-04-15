const MAILGUN_API_KEY = MAILGUN_API_KEY;
const MAILGUN_DOMAIN = MAILGUN_DOMAIN;
const FROM_EMAIL = `Berkley Security <mailgun@${MAILGUN_DOMAIN}>`;
const TO_EMAIL = 'staff@berkleysecurity.com';

async function sendEmail(name, email, phone, serviceArea, serviceType, propertyType, message) {
  const formData = new URLSearchParams();
  formData.append('from', FROM_EMAIL);
  formData.append('to', TO_EMAIL);
  formData.append('subject', `New Contact Form Submission from ${name}`);
  formData.append('html', `
    <h2>New Contact Form Submission</h2>
    <p><strong>Name:</strong> ${name}</p>
    <p><strong>Email:</strong> ${email}</p>
    <p><strong>Phone:</strong> ${phone}</p>
    <p><strong>Service Area:</strong> ${serviceArea}</p>
    <p><strong>Service Type:</strong> ${serviceType}</p>
    <p><strong>Property Type:</strong> ${propertyType}</p>
    <p><strong>Message:</strong> ${message || 'No message provided'}</p>
  `);

  const response = await fetch(`https://api.mailgun.net/v3/${MAILGUN_DOMAIN}/messages`, {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${btoa('api:' + MAILGUN_API_KEY)}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData.toString(),
  });

  return response.ok;
}

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

addEventListener('fetch', event => {
  if (event.request.method === 'OPTIONS') {
    event.respondWith(new Response(null, { headers: corsHeaders }));
    return;
  }

  if (event.request.method !== 'POST') {
    event.respondWith(new Response('Method not allowed', { status: 405, headers: corsHeaders }));
    return;
  }

  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  try {
    const contentType = request.headers.get('content-type') || '';
    
    let formData;
    if (contentType.includes('application/x-www-form-urlencoded')) {
      formData = await request.formData();
    } else if (contentType.includes('application/json')) {
      const body = await request.json();
      formData = new Map(Object.entries(body));
    } else if (contentType.includes('multipart/form-data')) {
      formData = await request.formData();
    } else {
      const text = await request.text();
      const params = new URLSearchParams(text);
      formData = new Map(params.entries());
    }

    const name = formData.get('name') || '';
    const email = formData.get('email') || '';
    const phone = formData.get('phone') || '';
    const serviceArea = formData.get('service-area') || formData.get('serviceArea') || '';
    const serviceType = formData.get('service-type') || formData.get('serviceType') || '';
    const propertyType = formData.get('property-type') || formData.get('propertyType') || '';
    const message = formData.get('message') || '';

    if (!name || !email || !phone) {
      return new Response(JSON.stringify({ error: 'Name, email, and phone are required' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return new Response(JSON.stringify({ error: 'Invalid email address' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const success = await sendEmail(name, email, phone, serviceArea, serviceType, propertyType, message);

    if (success) {
      return new Response(JSON.stringify({ success: true, message: 'Email sent successfully' }), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    } else {
      return new Response(JSON.stringify({ error: 'Failed to send email' }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }
  } catch (error) {
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
}