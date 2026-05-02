"""
JEE Success System - Study Data
Complete syllabus, resources, and earning opportunities
"""

# ─────────────────────────────────────────────────────────────────────────────
# FULL JEE SYLLABUS  (chapter → topics → PYQs → books)
# ─────────────────────────────────────────────────────────────────────────────
PHYSICS_CHAPTERS = [
    {
        "id": "phy_01", "name": "Units & Dimensions", "week": 1,
        "topics": ["SI Units", "Dimensional Analysis", "Significant Figures"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-1, Q1–Q20",
        "practice": "Arihant Physics: Exercise 1.1–1.3 (Q1–Q30)",
        "time_min": 30, "questions": 15, "difficulty": 1,
        "tip": "Master unit conversion first — it's asked every year."
    },
    {
        "id": "phy_02", "name": "Kinematics – 1D Motion", "week": 1,
        "topics": ["Distance vs Displacement", "Velocity & Acceleration", "Equations of Motion", "Graphs"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-2, Q1–Q25",
        "practice": "Arihant Physics: Exercise 2.1–2.4 (Q1–Q40)",
        "time_min": 40, "questions": 20, "difficulty": 2,
        "tip": "Draw v-t graphs for every problem — it saves time in JEE."
    },
    {
        "id": "phy_03", "name": "Kinematics – 2D Motion", "week": 1,
        "topics": ["Projectile Motion", "Relative Motion", "Circular Motion Basics"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-3, Q1–Q25",
        "practice": "Arihant Physics: Exercise 3.1–3.3 (Q1–Q35)",
        "time_min": 40, "questions": 20, "difficulty": 2,
        "tip": "Projectile: always split into horizontal + vertical components."
    },
    {
        "id": "phy_04", "name": "Laws of Motion", "week": 2,
        "topics": ["Newton's Laws", "Friction", "Pseudo Force", "Connected Bodies"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-4, Q1–Q30",
        "practice": "Arihant Physics: Exercise 4.1–4.5 (Q1–Q50)",
        "time_min": 45, "questions": 20, "difficulty": 3,
        "tip": "FBD (Free Body Diagram) for every problem — no exceptions."
    },
    {
        "id": "phy_05", "name": "Work, Energy & Power", "week": 2,
        "topics": ["Work done by variable force", "KE-PE theorem", "Conservation of Energy", "Power"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-5, Q1–Q25",
        "practice": "Arihant Physics: Exercise 5.1–5.4 (Q1–Q40)",
        "time_min": 40, "questions": 20, "difficulty": 3,
        "tip": "Use energy conservation — it's faster than Newton's laws for most problems."
    },
    {
        "id": "phy_06", "name": "Rotational Motion", "week": 3,
        "topics": ["Torque", "Angular Momentum", "MOI", "Rolling Motion"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-7, Q1–Q30",
        "practice": "Arihant Physics: Exercise 7.1–7.5 (Q1–Q45)",
        "time_min": 50, "questions": 20, "difficulty": 4,
        "tip": "Memorize MOI formulas for standard bodies — 5 marks guaranteed."
    },
    {
        "id": "phy_07", "name": "Gravitation", "week": 3,
        "topics": ["Kepler's Laws", "Gravitational PE", "Satellites", "Escape Velocity"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-8, Q1–Q20",
        "practice": "Arihant Physics: Exercise 8.1–8.3 (Q1–Q30)",
        "time_min": 35, "questions": 15, "difficulty": 3,
        "tip": "Orbital velocity and escape velocity are asked every single year."
    },
    {
        "id": "phy_08", "name": "Thermodynamics", "week": 4,
        "topics": ["Laws of Thermodynamics", "Carnot Engine", "Entropy", "Processes"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-12, Q1–Q25",
        "practice": "Arihant Physics: Exercise 12.1–12.4 (Q1–Q40)",
        "time_min": 45, "questions": 20, "difficulty": 4,
        "tip": "P-V diagrams are key — practice identifying the process type first."
    },
    {
        "id": "phy_09", "name": "Waves & Sound", "week": 4,
        "topics": ["Wave Equation", "Superposition", "Beats", "Doppler Effect"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-15, Q1–Q25",
        "practice": "Arihant Physics: Exercise 15.1–15.4 (Q1–Q40)",
        "time_min": 40, "questions": 20, "difficulty": 3,
        "tip": "Beats and Doppler Effect are high-yield topics in JEE Main."
    },
    {
        "id": "phy_10", "name": "Electrostatics", "week": 5,
        "topics": ["Coulomb's Law", "Electric Field", "Potential", "Capacitors"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-18, Q1–Q35",
        "practice": "Arihant Physics: Exercise 18.1–18.6 (Q1–Q60)",
        "time_min": 55, "questions": 25, "difficulty": 5,
        "tip": "Gauss's Law simplifies 80% of symmetric charge distribution problems."
    },
    {
        "id": "phy_11", "name": "Current Electricity", "week": 5,
        "topics": ["Ohm's Law", "Kirchhoff's Laws", "Wheatstone Bridge", "RC Circuits"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-20, Q1–Q30",
        "practice": "Arihant Physics: Exercise 20.1–20.5 (Q1–Q50)",
        "time_min": 50, "questions": 20, "difficulty": 4,
        "tip": "KVL/KCL is non-negotiable — practice circuit simplification daily."
    },
    {
        "id": "phy_12", "name": "Magnetism & EMI", "week": 6,
        "topics": ["Biot-Savart", "Ampere's Law", "Faraday's Law", "AC Circuits"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-22–24, Q1–Q35",
        "practice": "Arihant Physics: Exercise 22–24 (Q1–Q55)",
        "time_min": 55, "questions": 25, "difficulty": 5,
        "tip": "Lenz's Law direction — always use the right-hand rule, not intuition."
    },
    {
        "id": "phy_13", "name": "Optics", "week": 7,
        "topics": ["Reflection", "Refraction", "TIR", "Lens Formula", "Wave Optics"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-25–27, Q1–Q35",
        "practice": "Arihant Physics: Exercise 25–27 (Q1–Q55)",
        "time_min": 55, "questions": 25, "difficulty": 4,
        "tip": "Sign convention mistakes lose easy marks — be consistent."
    },
    {
        "id": "phy_14", "name": "Modern Physics", "week": 8,
        "topics": ["Photoelectric Effect", "Bohr Model", "Nuclear Physics", "Semiconductors"],
        "pyq_range": "Oswaal JEE PYQ Physics: Ch-29–32, Q1–Q40",
        "practice": "Arihant Physics: Exercise 29–32 (Q1–Q60)",
        "time_min": 55, "questions": 25, "difficulty": 4,
        "tip": "Modern Physics: highest marks-to-effort ratio in the entire syllabus."
    },
]

CHEMISTRY_CHAPTERS = [
    {
        "id": "chem_01", "name": "Mole Concept & Stoichiometry", "week": 1,
        "topics": ["Mole, Molarity, Molality", "Limiting Reagent", "Empirical Formula"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-1, Q1–Q25",
        "practice": "Arihant Chemistry: Exercise 1.1–1.4 (Q1–Q40)",
        "time_min": 35, "questions": 15, "difficulty": 2,
        "tip": "Memorise molar masses of first 30 elements — saves 2 mins per problem."
    },
    {
        "id": "chem_02", "name": "Atomic Structure", "week": 1,
        "topics": ["Bohr Model", "Quantum Numbers", "Orbitals", "Electronic Configuration"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-2, Q1–Q20",
        "practice": "Arihant Chemistry: Exercise 2.1–2.3 (Q1–Q30)",
        "time_min": 30, "questions": 15, "difficulty": 2,
        "tip": "Aufbau + Hund + Pauli — these three rules solve 90% of config questions."
    },
    {
        "id": "chem_03", "name": "Chemical Bonding", "week": 2,
        "topics": ["Ionic & Covalent Bonds", "VSEPR", "Hybridisation", "MOT Basics"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-4, Q1–Q30",
        "practice": "Arihant Chemistry: Exercise 4.1–4.5 (Q1–Q50)",
        "time_min": 40, "questions": 20, "difficulty": 3,
        "tip": "Bond angles — learn exceptions (NH3, H2O, SF6) separately."
    },
    {
        "id": "chem_04", "name": "Thermodynamics (Chem)", "week": 2,
        "topics": ["Enthalpy", "Entropy", "Gibbs Energy", "Hess's Law"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-6, Q1–Q25",
        "practice": "Arihant Chemistry: Exercise 6.1–6.4 (Q1–Q40)",
        "time_min": 40, "questions": 20, "difficulty": 3,
        "tip": "ΔG = ΔH − TΔS: memorise the four cases (sign combinations)."
    },
    {
        "id": "chem_05", "name": "Equilibrium", "week": 3,
        "topics": ["Kp, Kc, Kx", "Le Chatelier's Principle", "Acid-Base Equilibrium", "pH"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-7, Q1–Q30",
        "practice": "Arihant Chemistry: Exercise 7.1–7.5 (Q1–Q50)",
        "time_min": 45, "questions": 20, "difficulty": 4,
        "tip": "Buffer solution problems are high-frequency — practice Henderson equation."
    },
    {
        "id": "chem_06", "name": "Redox Reactions", "week": 3,
        "topics": ["Oxidation State", "Balancing by HM & ION", "Disproportionation"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-8, Q1–Q20",
        "practice": "Arihant Chemistry: Exercise 8.1–8.3 (Q1–Q30)",
        "time_min": 30, "questions": 15, "difficulty": 3,
        "tip": "Always write half-reactions — balancing is mechanical once you know it."
    },
    {
        "id": "chem_07", "name": "Organic Chemistry Basics", "week": 4,
        "topics": ["IUPAC", "Isomerism", "Inductive/Resonance Effects", "Reaction Intermediates"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-12, Q1–Q30",
        "practice": "Arihant Chemistry: Exercise 12.1–12.5 (Q1–Q50)",
        "time_min": 50, "questions": 20, "difficulty": 4,
        "tip": "Resonance structures — draw ALL of them, don't skip any."
    },
    {
        "id": "chem_08", "name": "Hydrocarbons", "week": 4,
        "topics": ["Alkanes/Alkenes/Alkynes", "Aromaticity", "Reactions", "Mechanisms"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-13, Q1–Q30",
        "practice": "Arihant Chemistry: Exercise 13.1–13.5 (Q1–Q50)",
        "time_min": 50, "questions": 20, "difficulty": 4,
        "tip": "Markovnikov's rule + Peroxide effect — always identify which applies."
    },
    {
        "id": "chem_09", "name": "Electrochemistry", "week": 5,
        "topics": ["Electrolytic Cell", "Galvanic Cell", "EMF", "Faraday's Laws"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-17, Q1–Q25",
        "practice": "Arihant Chemistry: Exercise 17.1–17.4 (Q1–Q40)",
        "time_min": 40, "questions": 20, "difficulty": 4,
        "tip": "Nernst equation is asked every year — learn to apply it in 30 seconds."
    },
    {
        "id": "chem_10", "name": "p-Block Elements", "week": 6,
        "topics": ["Group 13–18", "Oxides & Halides", "Allotropes", "Reactions"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-11, Q1–Q35",
        "practice": "Arihant Chemistry: Exercise 11.1–11.6 (Q1–Q55)",
        "time_min": 55, "questions": 25, "difficulty": 4,
        "tip": "p-block: 12-15 questions per year in JEE Main. High ROI chapter."
    },
    {
        "id": "chem_11", "name": "d & f Block + Coordination", "week": 7,
        "topics": ["Properties of TM", "Crystal Field Theory", "Isomerism in Complexes"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-9–10, Q1–Q30",
        "practice": "Arihant Chemistry: Exercise 9–10 (Q1–Q50)",
        "time_min": 50, "questions": 20, "difficulty": 4,
        "tip": "IUPAC naming of coordination compounds — learn the rules once, get 4 marks."
    },
    {
        "id": "chem_12", "name": "Biomolecules & Polymers", "week": 8,
        "topics": ["Carbs, Proteins, Nucleic Acids", "Polymers", "Chemistry in Daily Life"],
        "pyq_range": "Oswaal JEE PYQ Chemistry: Ch-23–25, Q1–Q25",
        "practice": "Arihant Chemistry: Exercise 23–25 (Q1–Q35)",
        "time_min": 35, "questions": 15, "difficulty": 2,
        "tip": "Pure memory chapter — 10 days of revision = 8 guaranteed marks."
    },
]

MATHS_CHAPTERS = [
    {
        "id": "math_01", "name": "Sets, Relations & Functions", "week": 1,
        "topics": ["Set Operations", "Types of Functions", "Domain/Range", "Composition"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-1–2, Q1–Q20",
        "practice": "Arihant Maths: Exercise 1–2 (Q1–Q35)",
        "time_min": 25, "questions": 10, "difficulty": 2,
        "tip": "Arrow diagrams for function types — visualise before algebraic approach."
    },
    {
        "id": "math_02", "name": "Algebra – Basics", "week": 1,
        "topics": ["Quadratic Equations", "Complex Numbers", "Progressions"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-3–5, Q1–Q30",
        "practice": "Arihant Maths: Exercise 3–5 (Q1–Q50)",
        "time_min": 30, "questions": 15, "difficulty": 2,
        "tip": "Quadratic: always check discriminant first. Saves time."
    },
    {
        "id": "math_03", "name": "Sequences & Series", "week": 1,
        "topics": ["AP, GP, HP", "Sum Formulas", "AGP", "Special Series"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-6, Q1–Q25",
        "practice": "Arihant Maths: Exercise 6 (Q1–Q40)",
        "time_min": 30, "questions": 15, "difficulty": 3,
        "tip": "AGP (Arithmetico-Geometric): method of differences — practice 10 problems."
    },
    {
        "id": "math_04", "name": "Permutation & Combination", "week": 2,
        "topics": ["nPr, nCr", "Circular Arrangement", "Multinomial", "Distribution"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-7, Q1–Q25",
        "practice": "Arihant Maths: Exercise 7 (Q1–Q40)",
        "time_min": 35, "questions": 15, "difficulty": 3,
        "tip": "Always decide: is order important? That determines P or C."
    },
    {
        "id": "math_05", "name": "Binomial Theorem", "week": 2,
        "topics": ["General Term", "Middle Term", "Binomial Coefficients", "Multinomial"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-8, Q1–Q20",
        "practice": "Arihant Maths: Exercise 8 (Q1–Q30)",
        "time_min": 30, "questions": 10, "difficulty": 3,
        "tip": "(r+1)th term formula — memorise it; most binomial questions use only this."
    },
    {
        "id": "math_06", "name": "Matrices & Determinants", "week": 3,
        "topics": ["Types of Matrices", "Operations", "Determinant Properties", "Inverse"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-9, Q1–Q25",
        "practice": "Arihant Maths: Exercise 9 (Q1–Q40)",
        "time_min": 40, "questions": 20, "difficulty": 4,
        "tip": "Determinant properties > expansion: use row/column operations to simplify."
    },
    {
        "id": "math_07", "name": "Trigonometry", "week": 3,
        "topics": ["Identities", "Equations", "Inverse Trig", "Heights & Distances"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-3–4 (Trigo), Q1–Q30",
        "practice": "Arihant Maths: Trigo Exercise (Q1–Q50)",
        "time_min": 45, "questions": 20, "difficulty": 3,
        "tip": "SinA+SinB, CosA+CosB formulas — your most used tools in Trigo."
    },
    {
        "id": "math_08", "name": "Straight Lines & Circles", "week": 4,
        "topics": ["Line Equations", "Angle Bisectors", "Circle Equations", "Tangent/Normal"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-10–11, Q1–Q30",
        "practice": "Arihant Maths: Exercise 10–11 (Q1–Q50)",
        "time_min": 45, "questions": 20, "difficulty": 4,
        "tip": "Family of lines concept: S + λS' = 0 — solves 40% of circle problems."
    },
    {
        "id": "math_09", "name": "Conic Sections", "week": 4,
        "topics": ["Parabola", "Ellipse", "Hyperbola", "Tangents & Normals"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-11, Q1–Q35",
        "practice": "Arihant Maths: Exercise 11 (Q1–Q55)",
        "time_min": 55, "questions": 25, "difficulty": 5,
        "tip": "Conics = highest weightage in coordinate geometry. No shortcuts — practice daily."
    },
    {
        "id": "math_10", "name": "Limits, Continuity & Differentiability", "week": 5,
        "topics": ["L'Hopital", "Sandwich Theorem", "Continuity Check", "Differentiability"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-13, Q1–Q30",
        "practice": "Arihant Maths: Exercise 13 (Q1–Q50)",
        "time_min": 50, "questions": 20, "difficulty": 4,
        "tip": "0/0 form: always try factorisation before L'Hopital's Rule."
    },
    {
        "id": "math_11", "name": "Differentiation & Applications", "week": 5,
        "topics": ["Chain Rule", "Implicit", "Maxima/Minima", "Tangent/Normal", "Rolle's Theorem"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-14, Q1–Q30",
        "practice": "Arihant Maths: Exercise 14 (Q1–Q50)",
        "time_min": 50, "questions": 20, "difficulty": 4,
        "tip": "AOD: check endpoints when finding global max/min on a closed interval."
    },
    {
        "id": "math_12", "name": "Integral Calculus", "week": 6,
        "topics": ["Standard Integrals", "By Parts", "Partial Fractions", "Definite Integrals", "Area"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-15, Q1–Q35",
        "practice": "Arihant Maths: Exercise 15 (Q1–Q60)",
        "time_min": 60, "questions": 25, "difficulty": 5,
        "tip": "King property of definite integrals solves 30% of JEE calculus problems."
    },
    {
        "id": "math_13", "name": "Vectors & 3D Geometry", "week": 7,
        "topics": ["Dot/Cross Product", "Lines in 3D", "Planes", "Distance Formulas"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-10–11 (3D), Q1–Q30",
        "practice": "Arihant Maths: 3D Exercise (Q1–Q50)",
        "time_min": 50, "questions": 20, "difficulty": 4,
        "tip": "Skew lines distance formula — high frequency, low effort to learn."
    },
    {
        "id": "math_14", "name": "Probability & Statistics", "week": 8,
        "topics": ["Classical Probability", "Conditional Prob", "Bayes' Theorem", "Distribution"],
        "pyq_range": "Oswaal JEE PYQ Maths: Ch-16, Q1–Q25",
        "practice": "Arihant Maths: Exercise 16 (Q1–Q40)",
        "time_min": 40, "questions": 20, "difficulty": 3,
        "tip": "Bayes' Theorem: always draw a tree diagram — avoids all confusion."
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# WEEKLY PLAN  (8 weeks × 7 days)
# ─────────────────────────────────────────────────────────────────────────────

def get_week_plan(week_number: int) -> dict:
    """Return the 7-day plan for a given week."""
    plans = {
        1: {
            "theme": "Foundation Week",
            "days": [
                {"day": 1, "phy": "phy_01", "chem": "chem_01", "math": "math_01", "status": "study"},
                {"day": 2, "phy": "phy_02", "chem": "chem_02", "math": "math_02", "status": "study"},
                {"day": 3, "phy": "phy_03", "chem": "chem_01", "math": "math_03", "status": "study"},
                {"day": 4, "phy": "phy_01", "chem": "chem_02", "math": "math_01", "status": "revision"},
                {"day": 5, "phy": "phy_02", "chem": "chem_01", "math": "math_02", "status": "practice"},
                {"day": 6, "phy": None, "chem": None, "math": None, "status": "mini_test", "test": "Ch 1 All Subjects", "test_time": 60},
                {"day": 7, "phy": None, "chem": None, "math": None, "status": "revision_day"},
            ]
        },
        2: {
            "theme": "Building Mechanics",
            "days": [
                {"day": 1, "phy": "phy_04", "chem": "chem_03", "math": "math_04", "status": "study"},
                {"day": 2, "phy": "phy_05", "chem": "chem_04", "math": "math_05", "status": "study"},
                {"day": 3, "phy": "phy_04", "chem": "chem_03", "math": "math_04", "status": "practice"},
                {"day": 4, "phy": "phy_05", "chem": "chem_04", "math": "math_05", "status": "practice"},
                {"day": 5, "phy": "phy_04", "chem": "chem_03", "math": "math_04", "status": "revision"},
                {"day": 6, "phy": None, "chem": None, "math": None, "status": "mini_test", "test": "Week 1–2 Chapters", "test_time": 60},
                {"day": 7, "phy": None, "chem": None, "math": None, "status": "revision_day"},
            ]
        },
    }
    # Default week for weeks 3–8
    default_plan = {
        "theme": f"Week {week_number} – Intermediate",
        "days": [
            {"day": d, "phy": None, "chem": None, "math": None, "status": "study"}
            for d in range(1, 8)
        ]
    }
    return plans.get(week_number, default_plan)


# ─────────────────────────────────────────────────────────────────────────────
# EARNING OPPORTUNITIES
# ─────────────────────────────────────────────────────────────────────────────
EARNING_GIGS = [
    {
        "title": "📝 Content Writing",
        "desc": "Write blogs, articles, product descriptions for clients.",
        "earning": "₹500–₹1500 per task",
        "time": "1–2 hrs",
        "skill": "Writing",
        "demand": "🔥 High Demand",
        "steps": [
            "1. Create a free account on Fiverr or Internshala",
            "2. Create a gig: 'I will write SEO articles (500 words)'",
            "3. Write 2–3 sample articles in your niche",
            "4. Deliver on time, build 5-star reviews",
            "5. Scale: ₹500 → ₹1500 per article within 2 weeks"
        ],
        "start_link": "https://www.fiverr.com"
    },
    {
        "title": "🎨 Graphic Designing",
        "desc": "Create posters, thumbnails, logos using Canva / Photoshop.",
        "earning": "₹300–₹1000 per design",
        "time": "1–3 hrs",
        "skill": "Canva / PS",
        "demand": "📈 Steady Demand",
        "steps": [
            "1. Learn Canva (free — 2-hour YouTube tutorial is enough)",
            "2. Create 5 sample thumbnails for YouTube channels",
            "3. Offer free designs to 3 small creators first (get reviews)",
            "4. List on Fiverr: 'YouTube Thumbnail Design ₹299'",
            "5. Upsell: logo packs, social media kits"
        ],
        "start_link": "https://www.canva.com"
    },
    {
        "title": "👨‍🏫 Online Tutoring",
        "desc": "Teach school students (Class 6–10) online.",
        "earning": "₹500–₹2000 per hour",
        "time": "1–2 hrs",
        "skill": "Teaching",
        "demand": "💎 High Value",
        "steps": [
            "1. List on UrbanPro or Superprof (free listing)",
            "2. Teach Maths/Science for Class 6–10 (you know this!)",
            "3. Start with ₹100/hr to get first 5 reviews",
            "4. Increase to ₹300/hr after 5 reviews",
            "5. Offer monthly packages: ₹2000/student/month"
        ],
        "start_link": "https://www.urbanpro.com"
    },
    {
        "title": "🎬 YouTube Automation",
        "desc": "Script, voiceover, and edit videos for faceless channels.",
        "earning": "₹1000–₹5000 per project",
        "time": "2–4 hrs",
        "skill": "Video Editing",
        "demand": "🚀 High Growth",
        "steps": [
            "1. Learn basics: CapCut (free) or DaVinci Resolve",
            "2. Pick a niche: motivation, facts, finance (no face needed)",
            "3. Use free stock footage (Pexels) + AI voiceover (ElevenLabs free)",
            "4. Offer editing service on Fiverr: ₹500 per video",
            "5. Scale: start your own channel after 3 months"
        ],
        "start_link": "https://www.capcut.com"
    },
    {
        "title": "💼 Freelance Assistant",
        "desc": "Data entry, research tasks, virtual assistant work.",
        "earning": "₹300–₹800 per task",
        "time": "1–2 hrs",
        "skill": "Basic Computer",
        "demand": "✅ Steady Income",
        "steps": [
            "1. Register on Truelancer or Freelancer.in (free)",
            "2. Apply for: data entry, web research, Excel tasks",
            "3. Bid low initially (₹200/task) to win first projects",
            "4. Deliver fast and accurate — 5-star reviews are your asset",
            "5. Aim: 2–3 tasks/day = ₹600–₹2400/day extra"
        ],
        "start_link": "https://www.truelancer.com"
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# MOTIVATIONAL QUOTES
# ─────────────────────────────────────────────────────────────────────────────
QUOTES = [
    "🔥 Discipline today, success tomorrow. — JEE Success System",
    "💪 Small steps every day lead to big results one day.",
    "🎯 The pain you feel today will be the strength you feel tomorrow.",
    "⚡ Consistency is the only shortcut. There is no other way.",
    "🏆 You don't have to be the smartest. Just be the most consistent.",
    "🚀 1% better every day = 37× better in a year. Start NOW.",
    "🌟 Every IITian was once exactly where you are. They didn't quit.",
    "💡 One more question today = one rank better tomorrow.",
    "🔑 Focus is not about saying yes. It's about saying NO to distractions.",
    "🎓 The journey is tough, but so are you. Keep going.",
    "⏰ Time wasted today is a rank lost tomorrow. Use it wisely.",
    "✅ A goal without a plan is just a wish. Execute your plan today.",
]

# ─────────────────────────────────────────────────────────────────────────────
# STUDY TIPS  (random daily tip)
# ─────────────────────────────────────────────────────────────────────────────
DAILY_TIPS = [
    "📖 Read theory first, then solve problems. Never the other way around.",
    "✏️ Write while you study — it improves retention by 40%.",
    "⏱️ Use Pomodoro: 25 min focused study + 5 min break.",
    "🔄 Revise yesterday's topic for 10 min before starting today's.",
    "📊 Track your mistakes in a separate notebook — review weekly.",
    "💤 Sleep 7–8 hours. Your brain consolidates memory during sleep.",
    "📵 Phone in another room while studying. Notifications kill focus.",
    "🎯 Set a specific target before each session: '15 questions in 30 min'.",
    "🗺️ Make mind maps for theory chapters — great for last-minute revision.",
    "⚡ Solve PYQs after every chapter. JEE repeats patterns every year.",
]

# ─────────────────────────────────────────────────────────────────────────────
# HELPER  — get chapter by ID
# ─────────────────────────────────────────────────────────────────────────────
_ALL_CHAPTERS = {c["id"]: c for c in PHYSICS_CHAPTERS + CHEMISTRY_CHAPTERS + MATHS_CHAPTERS}

def get_chapter(chapter_id: str) -> dict | None:
    return _ALL_CHAPTERS.get(chapter_id)

def get_chapters_by_week(week: int) -> dict:
    """Return {phy: [...], chem: [...], math: [...]} for the given week."""
    return {
        "phy": [c for c in PHYSICS_CHAPTERS if c["week"] == week],
        "chem": [c for c in CHEMISTRY_CHAPTERS if c["week"] == week],
        "math": [c for c in MATHS_CHAPTERS if c["week"] == week],
    }
