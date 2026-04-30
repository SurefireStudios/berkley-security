import os
import random
import re
from bs4 import BeautifulSoup

base_dir = r'c:\Users\Haz\Desktop\Berkley Security\city'

hero_variations = [
    "Safeguard your {city} property with AI-driven alarm systems, high-definition surveillance cameras, and 24/7 rapid-response monitoring. As the premier security provider for {county} since 1978, we deliver specialized protection for both residential and commercial spaces. Fully licensed in {state}.",
    "Defend your home and business in {city} with cutting-edge security systems, intelligent video surveillance, and round-the-clock professional monitoring. We are the trusted, long-standing security authority serving {county} families and enterprises since 1978. Fully insured and licensed in {state}.",
    "Elevate your security in {city} with custom-engineered alarm systems, 4K security cameras, and uninterrupted 24/7 monitoring. Berkley Security has been the definitive choice for comprehensive property protection across {county} since 1978. Licensed and certified in {state}.",
    "Protecting {city} with industry-leading alarm technology, comprehensive camera installation, and 24/7 dedicated monitoring. Recognized as the top security contractor in {county} for over four decades, we secure homes and commercial facilities with precision. Licensed in {state}.",
    "Ensure total peace of mind in {city} with state-of-the-art security alarms, smart surveillance cameras, and elite 24/7 monitoring services. As a deeply rooted, local provider serving {county} since 1978, our licensed experts build systems that actually stop threats. Licensed in {state}."
]

intro_p1_variations = [
    "Implementing the most effective security system in {city}, {state} requires an installation team that actually understands the local environment. Whether your property is located in the bustling commercial center or the quieter, rural expanses of {county}, you face distinct security challenges that demand a hyper-customized approach.",
    "Finding the top-rated security provider in {city}, {state} means partnering with experts who know the region intimately. From suburban neighborhoods to the sprawling agricultural and industrial zones of {county}, the security threats vary drastically, requiring customized, high-performance solutions rather than generic kits.",
    "When evaluating the best security systems in {city}, {state}, local expertise is non-negotiable. The landscape of {county} presents unique vulnerabilities—from urban retail theft to remote property intrusion—which is why an off-the-shelf system simply is not enough to guarantee your safety.",
    "The foundation of reliable security in {city}, {state} is localized, professional engineering. Because {county} encompasses a diverse mix of residential communities and robust commercial districts, your property requires a tailored security infrastructure designed to neutralize its specific risks.",
    "Securing your property in {city}, {state} starts with choosing a security company that understands the local threat landscape. The varied environments across {county} mean that a one-size-fits-all approach leaves vulnerabilities exposed. We design systems engineered specifically for your exact location."
]

intro_p2_variations = [
    "Whether you are looking to install a robust home security system for your family, advanced IP cameras for your small business, or a comprehensive access control and intrusion system for a large {county} warehouse, our certified technicians engineer the perfect defense. We refuse to sell pre-packaged, cookie-cutter systems because your {city} property requires individualized protection.",
    "If you need an intelligent home automation and alarm system, a multi-camera network for a retail storefront, or industrial-grade security for an agricultural facility in {county}, our specialized team delivers. We meticulously design and install every component, guaranteeing that no two {city} security systems are exactly alike.",
    "From residential burglar alarms to commercial-grade video surveillance and advanced fire detection, we provide end-to-end security solutions across {county}. Our licensed installers conduct a thorough threat assessment of your {city} property to ensure we deploy a system that actively deters crime, rather than just recording it.",
    "Our expertise covers the full spectrum of security technology: smart home alarms, commercial surveillance networks, enterprise access control, and industrial fire systems. Because every building in {city} has distinct access points and blind spots, we custom-build every system from the ground up to protect your specific {county} property.",
    "We specialize in comprehensive security engineering for both residential and commercial clients across {county}. Whether outfitting a {city} medical office with strict access control or securing a private home with smart locks and perimeter cameras, our technicians deploy enterprise-grade hardware tailored to your exact floorplan."
]

intro_p3_variations = [
    "Berkley Security has been the undisputed leader in protecting properties across Louisiana and Mississippi since 1978. Every installation we complete in {city} is backed by continuous 24/7 professional monitoring, rapid dispatch to local {county} law enforcement, seamless smartphone control, and a full 1-year warranty on parts and labor.",
    "Since 1978, Berkley Security has set the gold standard for life safety and property protection in Louisiana and Mississippi. Our {city} clients benefit from proactive 24/7 monitoring, immediate coordination with {county} first responders, intuitive mobile app access, and an unconditional 1-year parts and labor warranty.",
    "With a proven track record dating back to 1978, Berkley Security remains the most trusted name in regional protection across Louisiana and Mississippi. We equip every {city} property with unwavering 24/7 monitoring, direct links to {county} dispatchers, cutting-edge remote access, and a comprehensive 1-year warranty.",
    "For over 45 years, Berkley Security has defended homes and businesses throughout Louisiana and Mississippi. Every system installed in {city} features highly responsive 24/7 professional monitoring, instant alerts to {county} authorities, full smartphone integration, and an ironclad 1-year warranty covering both parts and labor.",
    "As the premier regional security firm since 1978, Berkley Security delivers unmatched reliability across Louisiana and Mississippi. Your {city} installation guarantees elite 24/7 monitoring, rapid communication with {county} emergency services, total remote control from anywhere in the world, and a 100% covered 1-year warranty."
]

serv_home_vars = [
    "Experience 24/7 monitored intrusion detection backed by instant police dispatch. We secure your {city} home using advanced door/window contacts, AI-driven motion sensors, glass break detection, and intuitive smart keypads. Protection begins with a comprehensive, free on-site threat assessment.",
    "Defend your {city} residence with elite 24/7 monitored burglar alarms and rapid emergency dispatch. Our home systems feature smart keypads, precision motion detectors, and comprehensive perimeter sensors. Schedule a free local assessment to identify your property's specific vulnerabilities.",
    "Achieve total peace of mind with continuous 24/7 intrusion monitoring and immediate law enforcement dispatch. We outfit {city} homes with state-of-the-art perimeter defense, glass break sensors, and intelligent control panels. Every residential installation starts with a free, custom security audit."
]

serv_cam_vars = [
    "Deploy high-definition 4K indoor and outdoor surveillance cameras equipped with color night vision, cloud/NVR storage, and real-time remote viewing. Perfectly engineered to monitor your {city} property 24/7, our camera systems deliver instant, AI-filtered motion alerts directly to your smartphone.",
    "Upgrade to commercial-grade IP security cameras featuring superior night vision, local NVR recording, and secure cloud backup. Whether monitoring a {city} storefront or residential perimeter, our video systems provide crystal-clear remote viewing and intelligent motion notifications.",
    "Keep a continuous watch over your {city} property with our advanced HD surveillance solutions. Featuring weather-proof outdoor cameras, wide dynamic range, and seamless mobile app integration, our video networks ensure you never miss a critical event, sending instant alerts straight to your device."
]

serv_biz_vars = [
    "Protect your enterprise with commercial-grade intrusion detection, scalable access control, and unwavering 24/7 monitoring. We specialize in securing {city} retail storefronts, medical facilities, vast warehouses, and corporate offices against internal and external threats.",
    "Safeguard your {city} business assets with enterprise-level security alarms, employee access control systems, and rapid-response 24/7 monitoring. We engineer custom commercial defenses for retail, healthcare, industrial, and office environments across {county}.",
    "Deploy uncompromising commercial security featuring advanced perimeter alarms, keyless access control, and immediate 24/7 professional monitoring. We build highly resilient security networks for {city} businesses, protecting inventory, staff, and facilities of all sizes."
]

serv_fire_vars = [
    "Ensure absolute life safety with code-compliant commercial and residential fire detection systems. Featuring rapid automatic fire department dispatch, our {city} installations utilize advanced smoke, heat, and carbon monoxide sensors. Complete annual inspection services are available.",
    "Defend your {city} property against devastating fire loss with our state-of-the-art, code-compliant fire alarm systems. We install highly sensitive smoke, heat, and CO detectors linked to instant emergency dispatch. We also provide mandatory annual fire inspections for commercial spaces.",
    "Mitigate disaster with heavily monitored, code-compliant fire alarm infrastructure. Our {city} technicians install intelligent smoke and heat detection systems that instantly alert local fire departments. We ensure your commercial or residential property meets all local safety regulations."
]

serv_med_vars = [
    "Provide critical independence for seniors and those with medical conditions in {city} with our rapid-response medical alert systems. A single press instantly connects to highly trained operators who dispatch EMS. Features robust cellular connectivity—no landline required.",
    "Ensure immediate help is always available with our specialized medical alert devices for {city} residents. Featuring simple one-button activation and built-in cellular technology, our systems instantly connect users to emergency dispatchers, functioning flawlessly without a traditional home phone line.",
    "Deliver life-saving response times for elderly or at-risk individuals in {city} via our advanced medical alert systems. Operating on reliable cellular networks, these wearable devices connect to trained medical dispatchers within seconds, ensuring rapid EMS response when it matters most."
]

serv_auto_vars = [
    "Transform your {city} property with intelligent home automation. Seamlessly control smart locks, responsive lighting, and advanced thermostats directly from your smartphone. Our automation technology integrates perfectly with your Berkley security panel for unified, effortless control.",
    "Elevate your {city} lifestyle with fully integrated smart home automation. Remotely manage motorized locks, energy-efficient thermostats, and automated lighting schedules. Our smart technology connects directly to your security system, giving you complete command of your property from anywhere.",
    "Take total control of your {city} home with advanced automation features. Utilize your smartphone to adjust smart thermostats, engage smart locks, and activate custom security scenes. Everything is seamlessly tied into your central Berkley security hub for maximum convenience and safety."
]

why_1_vars = [
    ("The Premier Local Security Authority", "We are not a disconnected national call center. Berkley Security is a deeply rooted, regional company actively serving Louisiana and Mississippi. Our technicians are localized to your area, resulting in significantly faster response times, accountability, and transparent pricing without hidden fees."),
    ("A Trusted Regional Security Partner", "Avoid the pitfalls of massive national chains. Berkley Security operates locally across Louisiana and Mississippi, meaning our technicians are familiar with your specific community. We deliver rapid, personalized service, exceptional local accountability, and strictly honest pricing models."),
    ("Locally Owned and Operated Expertise", "We pride ourselves on being a regional security leader, not an outsourced national corporation. Our deep presence in Louisiana and Mississippi allows our local technicians to provide expedited emergency service, unparalleled system knowledge, and straightforward, fair pricing.")
]

why_2_vars = [
    ("Fully Licensed & Vetted Technicians", "Every technician we employ is strictly background-checked, fully insured, and state-licensed before ever stepping foot on your property. We maintain the highest standards of integrity because your safety, privacy, and peace of mind are our absolute highest priorities."),
    ("Certified & Background-Checked Experts", "We never compromise on personnel. Each of our security installers undergoes rigorous background checks, holds active state licenses, and carries comprehensive insurance. Your security and personal privacy are handled with the utmost professional discretion and care."),
    ("Licensed Security Professionals", "Your security should only be handled by verified experts. Every Berkley technician is extensively vetted, insured, and licensed by the state. We enforce these strict hiring standards to ensure your property and privacy are always fully protected.")
]

why_3_vars = [
    ("Custom-Engineered Security Architecture", "We conduct comprehensive, on-site vulnerability assessments of your {city} property to engineer a security network tailored to your specific architectural and environmental needs. You receive an optimized defense system, never a generic package."),
    ("Precision System Design & Engineering", "Our experts physically inspect your {city} property to identify unique blind spots and access vulnerabilities. We then design and deploy a custom-built security infrastructure that precisely addresses your specific threats, avoiding ineffective one-size-fits-all kits."),
    ("Tailored Property Threat Assessments", "We don't guess when it comes to your safety. Our technicians evaluate your {city} property in person to map out security risks. We then formulate and install a highly specific security solution guaranteed to meet your exact defensive requirements.")
]

why_4_vars = [
    ("Elite 24/7 Professional Monitoring", "Our state-of-the-art monitoring center oversees your property 24/7, 365 days a year. Upon verifying an alarm, we instantly dispatch local {city} police, fire, or EMS. We also maintain a dedicated 24/7 rapid-response team for any critical system maintenance needs."),
    ("Uninterrupted 24/7 Emergency Monitoring", "Your property is actively protected around the clock by our highly trained monitoring staff. In the event of an emergency, we immediately coordinate with {city} first responders to ensure rapid intervention. Furthermore, our on-call technicians provide 24/7 support for system emergencies."),
    ("Continuous 24/7 Security Oversight", "We provide unwavering 24/7 monitoring every day of the year. The moment an alarm triggers, our team verifies the threat and dispatches {city} emergency services in seconds. We also offer specialized 24/7 emergency repair services to keep your system online.")
]

why_5_vars = [
    ("Comprehensive 1-Year Warranty", "Every security and camera installation is fully protected by our robust 1-year warranty covering 100% of parts and labor. If a component fails, we replace or repair it at zero cost. We unconditionally stand behind the reliability of every system we build in {county}."),
    ("Ironclad Parts & Labor Guarantee", "We guarantee our workmanship. Every installation is secured by a comprehensive 1-year warranty that includes all hardware and labor costs. Should any issue arise, we will resolve it entirely free of charge. We are fiercely committed to the quality of our {county} installations."),
    ("Full 1-Year System Warranty", "Your investment is safe with us. We back every new installation with a complete 1-year warranty covering both equipment and labor. If anything malfunctions, our technicians will fix it at absolutely no cost to you. We stand behind our work across all of {county}.")
]

final_cta_vars = [
    "Do not wait until a break-in or emergency forces your hand. Whether you require a smart home security system, a high-definition camera network for your business, or code-compliant fire protection for a commercial facility, the Berkley Security team is prepared to deliver. Call us today or request your free {city} property consultation online.",
    "Proactive security is the only effective security. Whether upgrading an outdated alarm, installing commercial surveillance cameras, or securing a new property with life safety systems, Berkley Security is your definitive partner. Contact our experts today to schedule your free, no-obligation security assessment in {city}.",
    "Take decisive action to protect your most valuable assets today. From residential smart alarms to enterprise-grade video surveillance and fire detection, the Berkley Security professionals are ready to secure your property. Reach out now by phone or online to claim your free security consultation in {city}."
]

cities = [f for f in os.listdir(base_dir) if f.endswith('.html')]
print(f'Starting rewrite of {len(cities)} files...')

for filename in cities:
    random.seed(filename) # Deterministic randomness based on filename
    file_path = os.path.join(base_dir, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Extract data
    title_tag = soup.find('title')
    title_text = title_tag.text if title_tag else ''
    city = 'your city'
    if ' in ' in title_text:
        city = title_text.split(' in ')[1].split(',')[0].strip()
        
    state = 'Mississippi' if '-ms' in filename else 'Louisiana'
    
    county = 'your county'
    # Find county in the hero section zip code p tag
    hero_p_tags = soup.find_all('p', class_=re.compile('.*uppercase.*'))
    for p in hero_p_tags:
        text = p.text
        if '-' in text:
            parts = text.split('-')
            if len(parts) >= 2:
                county = parts[1].strip()
                
    kwargs = {'city': city, 'state': state, 'county': county}
    
    # 1. Hero text
    hero_desc = soup.find('p', class_=re.compile('.*text-xl md:text-2xl.*'))
    if hero_desc:
        hero_desc.string = random.choice(hero_variations).format(**kwargs)
        
    # 2. Local Intro
    # It has 3 paragraphs inside the grid container after the h2 'X's Security Experts'
    intro_h2 = soup.find(lambda tag: tag.name == 'h2' and 'Security Experts' in ' '.join(tag.text.split()))
    if intro_h2:
        intro_div = intro_h2.find_parent('div')
        intro_ps = intro_div.find_all('p')
        if len(intro_ps) >= 3:
            intro_ps[0].string = random.choice(intro_p1_variations).format(**kwargs)
            intro_ps[1].string = random.choice(intro_p2_variations).format(**kwargs)
            intro_ps[2].string = random.choice(intro_p3_variations).format(**kwargs)
            
    # 3. Services Descriptions
    # Look for h3s inside the services section
    services_h2 = soup.find(lambda tag: tag.name == 'h2' and 'Security Services in' in ' '.join(tag.text.split()))
    if services_h2:
        services_section = services_h2.find_parent('section')
        h3s = services_section.find_all('h3')
        for h3 in h3s:
            p = h3.find_next_sibling('p')
            if not p: continue
            text = h3.text.lower()
            if 'home security' in text:
                p.string = random.choice(serv_home_vars).format(**kwargs)
            elif 'camera' in text or 'surveillance' in text:
                p.string = random.choice(serv_cam_vars).format(**kwargs)
            elif 'business' in text or 'alarm systems' in text:
                p.string = random.choice(serv_biz_vars).format(**kwargs)
            elif 'fire' in text:
                p.string = random.choice(serv_fire_vars).format(**kwargs)
            elif 'medical' in text:
                p.string = random.choice(serv_med_vars).format(**kwargs)
            elif 'automation' in text:
                p.string = random.choice(serv_auto_vars).format(**kwargs)
                
    # 4. Why Choose Us
    why_h2 = soup.find(lambda tag: tag.name == 'h2' and 'Choose Berkley Security' in ' '.join(tag.text.split()))
    if why_h2:
        why_div = why_h2.find_next_sibling('div')
        if why_div:
            items = why_div.find_all('div', recursive=False)
            if len(items) == 5:
                # 1
                h4 = items[0].find('h4')
                p = items[0].find('p')
                choice = random.choice(why_1_vars)
                h4.string = choice[0]
                p.string = choice[1].format(**kwargs)
                # 2
                h4 = items[1].find('h4')
                p = items[1].find('p')
                choice = random.choice(why_2_vars)
                h4.string = choice[0]
                p.string = choice[1].format(**kwargs)
                # 3
                h4 = items[2].find('h4')
                p = items[2].find('p')
                choice = random.choice(why_3_vars)
                h4.string = choice[0]
                p.string = choice[1].format(**kwargs)
                # 4
                h4 = items[3].find('h4')
                p = items[3].find('p')
                choice = random.choice(why_4_vars)
                h4.string = choice[0]
                p.string = choice[1].format(**kwargs)
                # 5
                h4 = items[4].find('h4')
                p = items[4].find('p')
                choice = random.choice(why_5_vars)
                h4.string = choice[0]
                p.string = choice[1].format(**kwargs)

    # 5. Final CTA
    cta_h2 = soup.find(lambda tag: tag.name == 'h2' and 'Ready to Protect Your' in ' '.join(tag.text.split()))
    if cta_h2:
        cta_p = cta_h2.find_next_sibling('p')
        if cta_p:
            cta_p.string = random.choice(final_cta_vars).format(**kwargs)
            
    # Write back to file, formatter preserves formatting well enough without messing up html structure
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))

print('Done rewriting 72 files.')
