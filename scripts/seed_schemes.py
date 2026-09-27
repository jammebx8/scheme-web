"""
Seed script: inserts 25 real Indian government schemes into Supabase.
Run: python scripts/seed_schemes.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "backend", ".env"))

from supabase import create_client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]
db = create_client(SUPABASE_URL, SUPABASE_KEY)

SCHEMES = [
    {
        "scheme_name": "PM Kisan Samman Nidhi",
        "slug": "pm-kisan-samman-nidhi",
        "details": "The PM-KISAN scheme provides financial support of ₹6,000 per year to all land-holding farmer families across India, paid in three equal installments of ₹2,000 every four months directly into their bank accounts.",
        "benefits": "₹6,000 per year (₹2,000 × 3 installments) directly into bank account via DBT. No repayment required.",
        "eligibility": "All land-holding farmer families with cultivable land. Excludes income tax payers, constitutional post holders, and families with a member who is or was a government servant earning ₹10,000+ per month.",
        "application": "https://pmkisan.gov.in",
        "documents": "Aadhaar card, Land records/Khasra-Khatauni, Bank account passbook, Mobile number",
        "level": "Central",
        "scheme_category": "Agriculture",
        "tags": ["farmer", "kisan", "income support", "direct benefit transfer", "pm kisan"],
    },
    {
        "scheme_name": "PM Fasal Bima Yojana",
        "slug": "pm-fasal-bima-yojana",
        "details": "Pradhan Mantri Fasal Bima Yojana provides comprehensive insurance coverage against crop failure due to non-preventable natural risks such as drought, flood, cyclone, storms, diseases, and pests.",
        "benefits": "Insurance coverage for crop losses due to natural calamities. Premium: 2% for Kharif, 1.5% for Rabi, 5% for commercial/horticulture crops. Full sum insured for losses above threshold.",
        "eligibility": "All farmers including sharecroppers and tenant farmers growing notified crops in notified areas. Both loanee and non-loanee farmers are eligible.",
        "application": "https://pmfby.gov.in",
        "documents": "Aadhaar card, Land records/7/12 extract, Bank passbook, Sowing certificate",
        "level": "Central",
        "scheme_category": "Agriculture",
        "tags": ["farmer", "crop insurance", "fasal bima", "kharif", "rabi"],
    },
    {
        "scheme_name": "PM Awas Yojana (Urban)",
        "slug": "pm-awas-yojana-urban",
        "details": "PMAY-Urban provides housing for all urban poor by 2024. Beneficiaries receive credit-linked subsidy for home loans, affordable housing in partnership with private sector, and in-situ slum redevelopment.",
        "benefits": "Interest subsidy of up to 6.5% on home loans for EWS/LIG categories; up to 3% for MIG-I; up to 4% for MIG-II. Maximum loan tenure of 20 years.",
        "eligibility": "EWS (annual income ≤₹3L), LIG (₹3L-₹6L), MIG-I (₹6L-₹12L), MIG-II (₹12L-₹18L). Applicant or family must not own a pucca house anywhere in India.",
        "application": "https://pmaymis.gov.in",
        "documents": "Aadhaar card, Income certificate, Bank account details, Address proof, Self-certification of not owning a house",
        "level": "Central",
        "scheme_category": "Housing",
        "tags": ["housing", "awas yojana", "home loan subsidy", "EWS", "LIG", "urban"],
    },
    {
        "scheme_name": "PM Awas Yojana (Gramin)",
        "slug": "pm-awas-yojana-gramin",
        "details": "PMAY-Gramin provides assistance for construction of pucca houses to all houseless and those living in dilapidated houses in rural areas across India.",
        "benefits": "₹1.20 lakh for plain areas, ₹1.30 lakh for hilly/difficult terrain. Additional ₹12,000 for toilet construction under Swachh Bharat Mission. Wages for 90-95 person-days under MGNREGS.",
        "eligibility": "Houseless families and those with zero, one, or two room kutcha/semi-pucca house in rural areas. Priority to SC/ST, minorities, people affected by bonded labour, widows, ex-servicemen, and disabled.",
        "application": "https://pmayg.nic.in",
        "documents": "Aadhaar card, BPL card, Bank passbook, SECC data enrollment",
        "level": "Central",
        "scheme_category": "Housing",
        "tags": ["housing", "rural", "gramin", "pucca house", "BPL"],
    },
    {
        "scheme_name": "PM Mudra Yojana",
        "slug": "pm-mudra-yojana",
        "details": "Pradhan Mantri MUDRA Yojana provides loans up to ₹10 lakh to non-corporate, non-farm small/micro enterprises through banks, MFIs and NBFCs. No collateral required.",
        "benefits": "Shishu: up to ₹50,000; Kishore: ₹50,001–₹5 lakh; Tarun: ₹5 lakh–₹10 lakh. No collateral security required. Concessional interest rates.",
        "eligibility": "Any Indian citizen with a business plan for non-farm income generating activities in manufacturing, trading and services sector. Small/micro enterprises, self-employed individuals, artisans, vegetable vendors, shopkeepers.",
        "application": "https://mudra.org.in",
        "documents": "Aadhaar, PAN, Business plan/proposal, Address proof, Bank statements (6 months), Proof of business existence",
        "level": "Central",
        "scheme_category": "Business & MSME",
        "tags": ["loan", "business", "mudra", "entrepreneur", "self-employed", "MSME"],
    },
    {
        "scheme_name": "Ayushman Bharat PM-JAY",
        "slug": "ayushman-bharat-pmjay",
        "details": "The world's largest government-funded health insurance scheme. Provides health cover of ₹5 lakh per family per year for secondary and tertiary care hospitalization.",
        "benefits": "Health insurance cover of ₹5 lakh per family per year. Covers 1,929 procedures including pre and post hospitalization. Cashless treatment at empaneled hospitals across India.",
        "eligibility": "Based on SECC-2011 database for rural families with specific deprivation criteria. Urban occupational categories including rag pickers, domestic workers, construction workers, beggars, etc.",
        "application": "https://pmjay.gov.in",
        "documents": "Aadhaar card, Ration card or SECC enrollment, Family composition proof",
        "level": "Central",
        "scheme_category": "Health",
        "tags": ["health", "insurance", "hospital", "ayushman", "5 lakh", "cashless treatment"],
    },
    {
        "scheme_name": "National Scholarship Portal - Merit-cum-Means",
        "slug": "nsp-merit-cum-means-scholarship",
        "details": "The Merit-cum-Means based scholarship for students of minority communities pursuing technical and professional courses. Offered through the National Scholarship Portal (NSP).",
        "benefits": "Course fee up to ₹20,000 per annum; Maintenance allowance ₹1,000 per month for hostellers, ₹500 for day scholars. 30% seats reserved for girl students.",
        "eligibility": "Students belonging to minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Zoroastrian) enrolled in technical/professional courses. Annual family income ≤₹2.5 lakh. Must have secured ≥50% marks in previous exam.",
        "application": "https://scholarships.gov.in",
        "documents": "Aadhaar card, Income certificate, Minority community certificate, Previous year marksheet, Fee receipt, Bank passbook",
        "level": "Central",
        "scheme_category": "Scholarship",
        "tags": ["scholarship", "minority", "student", "technical education", "NSP"],
    },
    {
        "scheme_name": "PM National Relief Fund Scholarship",
        "slug": "pm-national-relief-fund-scholarship",
        "details": "Scholarship for students whose parents/guardians died or became permanently disabled while performing their duty as Para Military and Armed Forces personnel.",
        "benefits": "₹2,000 per month for class IX-XII students; ₹3,000 per month for degree-level technical/medical/engineering courses.",
        "eligibility": "Wards of Central Armed Police Forces and Assam Rifles who died or were disabled in action/duty. Annual family income ≤₹6 lakh.",
        "application": "https://scholarships.gov.in",
        "documents": "Aadhaar, Marksheet, Income certificate, Service certificate of parent, Proof of death/disability in service",
        "level": "Central",
        "scheme_category": "Scholarship",
        "tags": ["scholarship", "paramilitary", "defence", "student", "NSP"],
    },
    {
        "scheme_name": "Sukanya Samriddhi Yojana",
        "slug": "sukanya-samriddhi-yojana",
        "details": "A government-backed savings scheme for the girl child providing high returns with tax benefits. Account can be opened at post offices and authorized banks.",
        "benefits": "Current interest rate ~8.2% per annum (compounded yearly). Tax-free returns under Section 80C. Premature closure allowed in case of life-threatening disease or marriage after 18 years.",
        "eligibility": "Indian resident parents/guardians of girl child below 10 years of age. Maximum two accounts per family (one per girl child).",
        "application": "https://www.indiapost.gov.in",
        "documents": "Birth certificate of girl child, Parent/guardian Aadhaar, PAN card, Address proof, Passport photo",
        "level": "Central",
        "scheme_category": "Women & Child",
        "tags": ["girl child", "savings", "sukanya", "education", "tax benefit"],
    },
    {
        "scheme_name": "PM Ujjwala Yojana",
        "slug": "pm-ujjwala-yojana",
        "details": "PMUY provides free LPG connections to women from Below Poverty Line (BPL) households and those from SC/ST, Pradhan Mantri Awas Yojana beneficiaries, Antodaya Anna Yojana beneficiaries, and other poor families.",
        "benefits": "Free LPG connection (14.2 kg cylinder + regulator + pipe + installation). First refill and hot plate provided free or at subsidized rates.",
        "eligibility": "Women from BPL households, SC/ST families, PM Awas Yojana (Gramin) beneficiaries, Antyodaya Anna Yojana households, forest dwellers, most backward classes, tea garden workers.",
        "application": "https://pmuy.gov.in",
        "documents": "Aadhaar card, BPL card or ration card, Bank passbook, Passport photo, Address proof",
        "level": "Central",
        "scheme_category": "Women & Child",
        "tags": ["LPG", "gas connection", "women", "BPL", "ujjwala", "kitchen"],
    },
    {
        "scheme_name": "PM Kaushal Vikas Yojana",
        "slug": "pm-kaushal-vikas-yojana",
        "details": "PMKVY provides free short-term skill training and certification to Indian youth. Training is provided by certified Training Partners and sector skill councils aligned with the National Skills Qualification Framework.",
        "benefits": "Free skill training (3 months to 1 year). Monetary reward of ₹8,000 on assessment and certification. Post-placement support and placement assistance. Recognition of Prior Learning (RPL) certification.",
        "eligibility": "Indian nationals between 15–45 years. School/college dropouts and unemployed youth. No income criteria specified.",
        "application": "https://www.pmkvyofficial.org",
        "documents": "Aadhaar card, Educational certificates, Bank passbook, Passport photo",
        "level": "Central",
        "scheme_category": "Skill Development",
        "tags": ["skill training", "youth", "employment", "PMKVY", "certification", "vocational"],
    },
    {
        "scheme_name": "Startup India Seed Fund Scheme",
        "slug": "startup-india-seed-fund",
        "details": "The Startup India Seed Fund Scheme provides financial assistance to startups for proof of concept, prototype development, product trials, market entry, and commercialization.",
        "benefits": "Up to ₹20 lakh for proof of concept/prototype/product trial (as grant). Up to ₹50 lakh for market entry/commercialization (as convertible debentures or debt). Through selected incubators.",
        "eligibility": "DPIIT-recognized startup. Startup incorporated not more than 2 years ago. Must not have received more than ₹10 lakh in monetary support from government schemes. Product/service with innovation and social impact.",
        "application": "https://seedfund.startupindia.gov.in",
        "documents": "DPIIT recognition certificate, Incorporation certificate, Business plan, Pitch deck, Team details, Bank account details",
        "level": "Central",
        "scheme_category": "Business & MSME",
        "tags": ["startup", "funding", "seed fund", "DPIIT", "entrepreneur", "innovation"],
    },
    {
        "scheme_name": "National Social Assistance Programme (NSAP)",
        "slug": "national-social-assistance-programme",
        "details": "NSAP provides social protection to poor households in the case of old age, death of breadwinner, maternity, and disability. Comprises Indira Gandhi National Old Age Pension Scheme, Widow Pension, and Disability Pension.",
        "benefits": "Old Age Pension: ₹200-₹500/month for 60-79 years; ₹500/month for 80+ years. Widow Pension: ₹300/month. Disability Pension: ₹300/month. Annapurna scheme: 10 kg foodgrains/month.",
        "eligibility": "BPL households. Old age: 60+ years. Widow: 40-79 years widow who is destitute. Disability: 80%+ disability below age 18-79 years. Income proof of poverty.",
        "application": "https://nsap.nic.in",
        "documents": "Aadhaar card, Age proof, BPL card, Bank passbook, Disability certificate (if applicable), Death certificate of husband (for widow pension)",
        "level": "Central",
        "scheme_category": "Pension",
        "tags": ["pension", "old age", "widow", "disability", "BPL", "social security", "NSAP"],
    },
    {
        "scheme_name": "Atal Pension Yojana",
        "slug": "atal-pension-yojana",
        "details": "Atal Pension Yojana focuses on the unorganized sector workers and provides fixed pension of ₹1,000–₹5,000 per month based on contribution, starting at age 60.",
        "benefits": "Fixed pension of ₹1,000, ₹2,000, ₹3,000, ₹4,000 or ₹5,000 per month at age 60. Spouse receives same pension after subscriber's death. Nominee receives corpus after both deaths.",
        "eligibility": "Indian citizen between 18-40 years of age with a bank account. Not a member of any statutory social security scheme (EPF, NPS, etc.).",
        "application": "https://npscra.nsdl.co.in/scheme-details.php",
        "documents": "Aadhaar card, Bank account details, Mobile number linked to bank",
        "level": "Central",
        "scheme_category": "Pension",
        "tags": ["pension", "retirement", "atal pension", "unorganized sector", "APY"],
    },
    {
        "scheme_name": "PM Jan Dhan Yojana",
        "slug": "pm-jan-dhan-yojana",
        "details": "PMJDY ensures access to financial services — banking/savings/deposit accounts, remittance, credit, insurance and pension — in an affordable manner to the excluded sections.",
        "benefits": "Zero balance savings account. RuPay debit card with ₹2 lakh accident insurance. ₹30,000 life cover. Overdraft facility up to ₹10,000. Access to pension and insurance schemes.",
        "eligibility": "Any Indian citizen above 10 years. No income limit. Those without a bank account or with only a basic savings bank deposit account.",
        "application": "Visit any bank branch or Business Correspondent",
        "documents": "Aadhaar card, or voter ID, or driving licence, or PAN card, or NREGA job card as identity/address proof",
        "level": "Central",
        "scheme_category": "Financial Inclusion",
        "tags": ["bank account", "jan dhan", "financial inclusion", "zero balance", "RuPay"],
    },
    {
        "scheme_name": "Pradhan Mantri Jeevan Jyoti Bima Yojana",
        "slug": "pm-jeevan-jyoti-bima-yojana",
        "details": "PMJJBY is a renewable term life insurance scheme offering life cover of ₹2 lakh for death due to any reason at a nominal premium of ₹330 per year.",
        "benefits": "₹2 lakh life insurance cover for death due to any cause. Annual premium of ₹330 auto-debited from bank account. Renewable annually.",
        "eligibility": "Indian citizens between 18-50 years of age with a bank or post office account. Premium auto-debit consent required.",
        "application": "Apply through bank branch, online banking, or PMJDY account",
        "documents": "Aadhaar card, Bank account, Mobile number",
        "level": "Central",
        "scheme_category": "Financial Inclusion",
        "tags": ["life insurance", "PMJJBY", "insurance", "low premium", "death benefit"],
    },
    {
        "scheme_name": "Pradhan Mantri Suraksha Bima Yojana",
        "slug": "pm-suraksha-bima-yojana",
        "details": "PMSBY offers accident insurance cover for death and disability due to accidents at a premium of just ₹20 per year, making it accessible to all.",
        "benefits": "₹2 lakh for accidental death or total disability. ₹1 lakh for partial disability. Annual premium of ₹20 auto-debited from bank account.",
        "eligibility": "Indian citizens between 18-70 years with a savings bank account. Premium auto-debit consent required.",
        "application": "Apply through bank branch, online banking, or CSC",
        "documents": "Aadhaar card, Bank account, Mobile number",
        "level": "Central",
        "scheme_category": "Financial Inclusion",
        "tags": ["accident insurance", "PMSBY", "disability", "low premium", "bank account"],
    },
    {
        "scheme_name": "National Apprenticeship Promotion Scheme",
        "slug": "national-apprenticeship-promotion-scheme",
        "details": "NAPS promotes apprenticeship training in India by sharing the cost of stipend to be paid to apprentices. It links industry with educational institutes to provide practical/on-job training.",
        "benefits": "25% of stipend (max ₹1,500/month) reimbursed to employers. Basic training cost reimbursed for apprentices without prior training. Apprenticeship certificates recognized nationally.",
        "eligibility": "Indian nationals between 14-21 years (up to 25 for SC/ST/PwD). Minimum 5th class pass. Registered on the National Apprenticeship Portal.",
        "application": "https://apprenticeshipindia.org",
        "documents": "Aadhaar card, Educational certificates, Bank passbook, Passport photo",
        "level": "Central",
        "scheme_category": "Skill Development",
        "tags": ["apprenticeship", "on-job training", "youth", "employment", "NAPS"],
    },
    {
        "scheme_name": "Beti Bachao Beti Padhao",
        "slug": "beti-bachao-beti-padhao",
        "details": "BBBP is a social campaign to generate awareness and improve efficiency of welfare services for girls in India. It focuses on preventing gender-biased sex selective elimination, ensuring survival and protection of the girl child, and promoting education.",
        "benefits": "Free education for girls up to Class 8 (RTE). Incentives under Sukanya Samriddhi Yojana. Scholarship for higher education. Conditional cash transfers in some states.",
        "eligibility": "Applicable to all girl children across India, especially in districts with low child sex ratio. Pregnant women and lactating mothers also included.",
        "application": "Apply through local Anganwadi or District Women and Child Development office",
        "documents": "Birth certificate, Aadhaar of parents, Address proof",
        "level": "Central",
        "scheme_category": "Women & Child",
        "tags": ["girl child", "education", "beti bachao", "gender equality", "scholarship"],
    },
    {
        "scheme_name": "Deen Dayal Upadhyaya Grameen Kaushalya Yojana",
        "slug": "ddu-grameen-kaushalya-yojana",
        "details": "DDU-GKY is a placement-linked skill training program for rural poor youth. It is part of the National Rural Livelihood Mission (NRLM) and targets youth between 15-35 years from BPL families.",
        "benefits": "Free skill training. ₹1,000–₹1,500 stipend during training. Residential training with boarding/lodging. Placement in jobs with ₹6,000+ per month salary. Post-placement support for 2 years.",
        "eligibility": "Rural youth between 15-35 years (up to 45 for SC/ST/PwD/women). At least 1 year of school education. Household income ≤₹1 lakh per annum or SECC enrolled.",
        "application": "https://ddugky.gov.in",
        "documents": "Aadhaar, Age proof, Educational certificate, Income/BPL certificate, Bank passbook, Passport photo",
        "level": "Central",
        "scheme_category": "Employment",
        "tags": ["skill training", "rural youth", "placement", "DDU-GKY", "employment", "BPL"],
    },
    {
        "scheme_name": "Mahatma Gandhi NREGA",
        "slug": "mahatma-gandhi-nrega",
        "details": "MGNREGS guarantees 100 days of wage employment per financial year to adult members of rural households who are willing to do unskilled manual work.",
        "benefits": "Guaranteed 100 days of wage employment at statutory minimum wages (₹220-₹333/day depending on state). Payment within 15 days. Compensation if employment not provided within 15 days.",
        "eligibility": "Adult members (18+) of rural households who are willing to do unskilled manual work. No income restrictions. Application through local Gram Panchayat.",
        "application": "Apply at local Gram Panchayat office or online at nregastrep.nic.in",
        "documents": "Job Card (apply at Gram Panchayat), Aadhaar, Bank passbook",
        "level": "Central",
        "scheme_category": "Employment",
        "tags": ["employment guarantee", "rural", "MGNREGS", "NREGA", "manual work", "wages"],
    },
    {
        "scheme_name": "Scholarship for Differently Abled Students",
        "slug": "scholarship-differently-abled-students",
        "details": "National Scholarship for Persons with Disabilities provides scholarship to disabled students pursuing studies from Class 9 to post-graduation. Offered through the Department of Empowerment of Persons with Disabilities.",
        "benefits": "Pre-matric: ₹800-₹1,200 per month. Post-matric: ₹900-₹1,500 per month. Top-class education: up to ₹2 lakh per annum for 11 prestigious institutions. Book/stationery allowance and disability-specific benefits.",
        "eligibility": "Students with benchmark disability (≥40% disability). Annual family income ≤₹2.5 lakh for pre-matric/post-matric; no income limit for Top Class. Enrolled in regular full-time courses.",
        "application": "https://scholarships.gov.in",
        "documents": "Aadhaar, Disability certificate from competent authority, Marksheet, Income certificate, Bank passbook, Admission fee receipt",
        "level": "Central",
        "scheme_category": "Differently Abled",
        "tags": ["disability", "scholarship", "PwD", "student", "differently abled"],
    },
    {
        "scheme_name": "PM Vishwakarma Scheme",
        "slug": "pm-vishwakarma-scheme",
        "details": "PM Vishwakarma provides end-to-end support to artisans and craftspeople who work with their hands and tools. It covers 18 traditional trades like blacksmith, goldsmith, potter, weaver, carpenter etc.",
        "benefits": "Recognition via PM Vishwakarma certificate and ID card. Skill training with ₹500/day stipend. Collateral-free loans: ₹1 lakh (1st tranche) at 5% interest, ₹2 lakh (2nd tranche). Digital payment incentive. Marketing support.",
        "eligibility": "Artisans and craftspersons in 18 traditional trades. Self-employed/unorganized sector. Family-based traditional work. Must not have availed PMEGP, PM SVANidhi, or Mudra loan in last 5 years.",
        "application": "https://pmvishwakarma.gov.in",
        "documents": "Aadhaar, Bank passbook, Mobile number, Declaration of traditional work, PAN (for loans above ₹50,000)",
        "level": "Central",
        "scheme_category": "Business & MSME",
        "tags": ["artisan", "craftsman", "vishwakarma", "skill", "loan", "traditional trades", "OBC"],
    },
    {
        "scheme_name": "PM Scholarship Scheme for Central Armed Police Forces",
        "slug": "pm-scholarship-capf",
        "details": "PM Scholarship Scheme for Central Armed Police Forces and Railway Protection Force provides scholarships to dependent wards of CAPF/RPF personnel for graduate-level technical and professional education.",
        "benefits": "₹3,000 per month for boys; ₹3,000 per month for girls (enhanced 2023). For 1st to 5th year of undergraduate technical courses only.",
        "eligibility": "Wards of deceased/ex-service personnel of CAPF (BSF, CRPF, CISF, ITBP, SSB, NSG, AR) and RPF. Must have scored ≥60% in 12th/Diploma. Enrolled in 1st year of technical/professional courses.",
        "application": "https://ksb.gov.in",
        "documents": "Aadhaar, Marksheet (12th), Admission letter, Service/discharge certificate of parent, Bank passbook",
        "level": "Central",
        "scheme_category": "Scholarship",
        "tags": ["scholarship", "CAPF", "paramilitary", "technical education", "defence"],
    },
    {
        "scheme_name": "Stand Up India Scheme",
        "slug": "stand-up-india-scheme",
        "details": "Stand-Up India facilitates bank loans between ₹10 lakh to ₹1 crore to at least one SC or ST borrower and at least one woman borrower per bank branch for setting up a greenfield enterprise.",
        "benefits": "Composite loan (working capital + term loan) of ₹10 lakh – ₹1 crore. Maximum 7-year repayment period with 18-month moratorium. Margin money: 25% with convergence from government schemes.",
        "eligibility": "SC/ST entrepreneurs or women entrepreneurs. Should be setting up a new (greenfield) enterprise in manufacturing, services, or trading. Loan for enterprise setup, not individuals.",
        "application": "https://www.standupmitra.in",
        "documents": "Aadhaar, PAN, SC/ST/woman certificate, Business plan, Address proof, Bank statements, Property documents (if mortgaged)",
        "level": "Central",
        "scheme_category": "Business & MSME",
        "tags": ["SC", "ST", "women entrepreneur", "startup loan", "stand up india", "greenfield"],
    },
]

def seed():
    print(f"Seeding {len(SCHEMES)} government schemes...")
    
    success = 0
    errors = 0
    
    for scheme in SCHEMES:
        try:
            # Check if already exists
            existing = db.table("government_schemes").select("id").eq("slug", scheme["slug"]).execute()
            if existing.data:
                print(f"  ⏭  Skip (exists): {scheme['scheme_name']}")
                continue
            
            result = db.table("government_schemes").insert(scheme).execute()
            if result.data:
                print(f"  ✅  Inserted: {scheme['scheme_name']}")
                success += 1
            else:
                print(f"  ❌  Failed: {scheme['scheme_name']}")
                errors += 1
        except Exception as e:
            print(f"  ❌  Error for {scheme['scheme_name']}: {e}")
            errors += 1
    
    print(f"\nDone! {success} inserted, {errors} errors, {len(SCHEMES) - success - errors} skipped (already exist).")

if __name__ == "__main__":
    seed()
