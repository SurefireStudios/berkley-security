export async function onRequestPost(context) {
  const { request, env } = context;

  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  try {
    const contentType = request.headers.get('content-type') || '';
    
    let formData;
    if (contentType.includes('application/x-www-form-urlencoded') || contentType.includes('multipart/form-data')) {
      formData = await request.formData();
    } else {
      const text = await request.text();
      const params = new URLSearchParams(text);
      formData = new Map(params.entries());
    }

    const name = formData.get('name') || '';
    const email = formData.get('email') || '';
    const phone = formData.get('phone') || '';
    const serviceArea = formData.get('service_area') || formData.get('service-area') || '';
    const serviceType = formData.get('service_type') || formData.get('service-type') || '';
    const propertyType = formData.get('property_type') || formData.get('property-type') || '';
    const message = formData.get('message') || '';
    const honeypot = formData.get('website') || '';

    // Honeypot check
    if (honeypot) {
      return new Response(JSON.stringify({ success: true, message: 'Message sent successfully.' }), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    if (!name || !email || !phone) {
      return new Response(JSON.stringify({ error: 'Name, email, and phone are required' }), {
        status: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    // Use environment variables for secrets
    const MAILGUN_API_KEY = env.MAILGUN_API_KEY;
    const MAILGUN_DOMAIN = env.MAILGUN_DOMAIN || "mg.berkleysecurity.com";
    const FROM_EMAIL = `Berkley Security Website <noreply@${MAILGUN_DOMAIN}>`;
    const TO_EMAIL = 'staff@berkleysecurity.com';

    if (!MAILGUN_API_KEY) {
      return new Response(JSON.stringify({ error: 'Server configuration error' }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const mailgunFormData = new URLSearchParams();
    mailgunFormData.append('from', FROM_EMAIL);
    mailgunFormData.append('to', TO_EMAIL);
    mailgunFormData.append('h:Reply-To', email);
    mailgunFormData.append('subject', `New Consultation Request from ${name} - ${serviceType}`);
    
    const htmlBody = `
      <h2>New Consultation Request</h2>
      <p><strong>Name:</strong> ${name}</p>
      <p><strong>Email:</strong> ${email}</p>
      <p><strong>Phone:</strong> ${phone}</p>
      <p><strong>Service Area:</strong> ${serviceArea}</p>
      <p><strong>Service Type:</strong> ${serviceType}</p>
      <p><strong>Property Type:</strong> ${propertyType}</p>
      <p><strong>Message:</strong> ${message || 'No message provided'}</p>
    `;
    mailgunFormData.append('html', htmlBody);

    const textBody = `
NEW CONSULTATION REQUEST
========================
Name: ${name}
Email: ${email}
Phone: ${phone}
Service Area: ${serviceArea}
Service Type: ${serviceType}
Property Type: ${propertyType}
Message: ${message || 'No message provided'}
    `;
    mailgunFormData.append('text', textBody);

    const response = await fetch(`https://api.mailgun.net/v3/${MAILGUN_DOMAIN}/messages`, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${btoa('api:' + MAILGUN_API_KEY)}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: mailgunFormData.toString(),
    });

    if (response.ok) {
      return new Response(JSON.stringify({ success: true, message: 'Your request has been sent successfully.' }), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    } else {
      console.error('Mailgun error:', await response.text());
      return new Response(JSON.stringify({ error: 'Failed to send email via Mailgun' }), {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }
  } catch (error) {
    console.error('Function error:', error);
    return new Response(JSON.stringify({ error: 'Internal server error processing the request' }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    }
  });
}
