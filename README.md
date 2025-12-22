# 📜 LegalAssist - Legal Awareness System

A Python + PyQt5 desktop application for providing **legal awareness and rights-based guidance** to Indian citizens in real-life situations.

## 🎯 What is LegalAssist?

LegalAssist is **NOT a lawyer** and does **NOT provide legal advice**. Instead, it:

✅ **Explains relevant laws** in simple, understandable language  
✅ **Clarifies your rights** according to the Constitution and Indian Penal Code  
✅ **Maps situations to applicable laws** using intelligent keyword matching  
✅ **Handles Hinglish & broken English** – understands real-world language  
✅ **Works offline** – no internet required after installation  
✅ **Shows confidence scores** – lets you know match reliability  

### Example
**User says:** "police ne roka aur parents ko call karne ko bola"  
**System understands:** Police harassment, unlawful stop, minor/guardian contact  
**System explains:** Article 19 (freedom), IPC 341 (wrongful restraint), your rights  

---

## 🏗️ Architecture Overview

### Three-Layer Design

```
┌─────────────────────────────────────────────┐
│  USER INPUT (Hinglish/Hindi/English)       │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  NORMALIZER (Text Preprocessing)            │
│  - Lowercase, remove punctuation            │
│  - Hinglish → English translation           │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  MATCHER (Keyword → Signals)                │
│  Scans keywords.json                        │
│  Produces semantic signals                  │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  RESOLVER (Signals → Situations)            │
│  References situations.json                 │
│  Calculates confidence (0-100%)             │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  LAW RETRIEVER (Situation → Laws)           │
│  Loads from laws.json                       │
│  Returns applicable legal references        │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  OUTPUT (Structured Result with Score)      │
└─────────────────────────────────────────────┘
```

### Data Files

**1. keywords.json** (Language Understanding)
- 17 keyword categories (AUTHORITY_POLICE, STOP_DETAIN, HARASSMENT_VERBAL, etc.)
- English, Hindi, Hinglish keywords for each category
- Global, reusable across all situations

**2. situations.json** (Legal Logic)
- 9 pre-defined legal situations
- Defines required + optional signals for each situation
- Maps to applicable laws

**3. laws.json** (Legal Knowledge)
- 16 Indian laws (Constitution, IPC, CrPC, IT Act, Juvenile Justice Act)
- Pure reference data: sections, titles, explanations, key points
- Includes "What You Can Ask" guidance

---

## 📦 Project Structure

```
legalassist/
├── main.py                          # PyQt GUI entry point
│
├── engine/
│   ├── normalizer.py               # Text preprocessing
│   ├── matcher.py                  # Core matching logic
│   └── resolver.py                 # Confidence scoring & ranking
│
├── data/
│   ├── keywords.json               # Language understanding layer
│   ├── situations.json             # Legal logic layer
│   └── laws.json                   # Legal knowledge layer
│
├── ui/
│   ├── styles.py                   # PyQt5 styling & themes
│   └── components.py               # Reusable UI widgets
│
├── utils/
│   └── translator.py               # Hindi/English conversion (optional)
│
├── requirements.txt                # Dependencies
├── setup.py                        # PyInstaller config
├── README.md                       # This file
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** (tested on 3.9, 3.10, 3.11)
- **Windows/macOS/Linux**
- ~200 MB disk space

### Installation

#### 1. Clone/Download Project

```bash
git clone https://github.com/yourusername/legalassist.git
cd legalassist
```

#### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run Application

```bash
python main.py
```

The PyQt5 window should open with the LegalAssist interface.

---

## 💻 Usage

### Basic Workflow

1. **Describe Your Situation**
   - Type in the text area (English, Hindi, or Hinglish)
   - Examples:
     - "police ne roka aur parents ko call karne ko bola"
     - "Police stopped me without reason and asked personal questions"
     - "मुझे गाली दी पुलिस ने"

2. **Click "Analyze & Find Laws"**
   - System processes your input
   - Normalizes text
   - Detects semantic signals
   - Matches to legal situations
   - Retrieves applicable laws

3. **Review Results**
   - **Situation Cards** show detected legal situation(s)
   - **Confidence Score** (0-100%) indicates match reliability
     - ≥80%: High confidence match
     - 50-80%: Medium confidence
     - <50%: Lower confidence (explore other matches)
   - **Applicable Laws** list relevant sections with explanations
   - **Key Points** highlight important legal aspects
   - **What You Can Ask** suggests polite, lawful questions

4. **Select Output Language**
   - English (default)
   - Hindi
   - Hinglish
   *(Language output feature expandable)*

---

## 🧠 How Matching Works

### Example: Police Harassment Case

**User Input:**
```
"I am walking with my sister, both 18+, police stopped us and asked why we are together and told us to call parents."
```

**Step 1: Normalization**
```
Normalized: "i am walking with my sister both 18 plus police stopped us and asked why we are together and told us to call parents"
```

**Step 2: Keyword Detection**
- **AUTHORITY_POLICE** ✓ (keyword: "police")
- **MOVEMENT_FREEDOM** ✓ (keyword: "walking")
- **RELATIONSHIP_INQUIRY** ✓ (keywords: "sister", "together")
- **AGE_ADULT** ✓ (keyword: "18+")
- **PARENT_CONTACT** ✓ (keyword: "call parents")
- **STOP_DETAIN** ✓ (keyword: "stopped")

**Step 3: Signal Matching**
```
Detected Signals: [
  AUTHORITY_POLICE,
  MOVEMENT_FREEDOM,
  RELATIONSHIP_INQUIRY,
  AGE_ADULT,
  PARENT_CONTACT,
  STOP_DETAIN
]
```

**Step 4: Situation Matching**
```
Situation: HARASSMENT_COUPLE
  Required: AUTHORITY_POLICE + RELATIONSHIP_INQUIRY + AGE_ADULT
  Optional: HARASSMENT_VERBAL, MOVEMENT_FREEDOM, PARENT_CONTACT
  
  Match Score: 100% (all required + 3/3 optional present)
```

**Step 5: Law Retrieval**
```
Applicable Laws:
- Article 19(1)(d): Freedom of Movement
- Article 21: Protection of Life and Personal Liberty
- IPC 509: Word/Gesture to Insult Modesty of Woman
- IPC 504: Intentional Insult with Knowledge of Causing Breach
```

**Step 6: Output Generation**
```
Situation: Harassment of Couple / Adults in Public
Confidence: 100%
Severity: MEDIUM

Laws:
1. Article 19(1)(d) - Freedom of Movement
   Explanation: Adults have right to move freely...
   
2. IPC 509 - Insult Modesty of Woman
   Key Points: ...

What You Can Politely Ask:
• Under which law are you stopping me?
• What is the legal basis for this inquiry?
• My personal relationships are not your concern
```

---

## 🔧 Customization & Extension

### Adding New Situations

1. **Identify the situation** (e.g., "Workplace Harassment")
2. **Add to situations.json**:
   ```json
   {
     "WORKPLACE_HARASSMENT": {
       "id": "WH001",
       "name": "Workplace Harassment",
       "required_signals": ["EMPLOYER", "HARASSMENT_VERBAL"],
       "optional_signals": ["THREAT_INTIMIDATION", "PRIVACY_VIOLATION"],
       "law_ids": ["LABOR_ACT_SECTION", ...],
       "severity": "medium"
     }
   }
   ```

3. **Add keywords** (if new signals needed):
   ```json
   "EMPLOYER": {
     "keywords": ["boss", "manager", "HR", "company", "employer"]
   }
   ```

4. **Add laws** (if new sections needed):
   ```json
   "LABOR_ACT_SECTION": {
     "id": "LABOR_ACT_SECTION",
     "type": "Labor Law",
     "section": "Section X",
     "title": "...",
     "explanation": "..."
   }
   ```

### Adding New Laws

Simply add to `laws.json`:
```json
{
  "NEW_LAW_ID": {
    "id": "NEW_LAW_ID",
    "type": "Law Type",
    "section": "Section X",
    "title": "Law Title",
    "explanation": "Clear explanation...",
    "key_points": ["Point 1", "Point 2"],
    "what_you_can_ask": ["Question 1", "Question 2"],
    "punishment_if_violated": "...",
    "references": ["Reference 1"]
  }
}
```

### Expanding Language Support

Currently supports: English, Hindi, Hinglish
To add regional languages:

1. Expand `keywords.json` with regional script keywords
2. Modify `normalizer.py` to handle new scripts
3. Add translation mappings for regional-to-English conversion

---

## 🎨 UI Features

### Modern PyQt5 Interface
- **Dark Theme** (professional, eye-friendly)
- **Responsive Layout** (adapts to window size)
- **Color-Coded Results**:
  - 🟢 Green (≥80% confidence)
  - 🟡 Orange (50-80% confidence)
  - 🔴 Red (<50% confidence)
- **Inline Citations** (referenced laws)
- **Scrollable Results** (handle multiple matches)
- **Legal Disclaimer** (prominent, always visible)

### Input Methods
- Multi-line text area (copy-paste friendly)
- Placeholder examples for guidance
- Clear button for quick reset

---

## ⚖️ Safety & Ethical Constraints

### What LegalAssist Does NOT Do

❌ Give legal advice  
❌ Encourage confrontation with police  
❌ Promote illegal activities  
❌ Replace a qualified lawyer  
❌ Guarantee outcomes  
❌ Provide tactical instructions  

### What LegalAssist ALWAYS Does

✅ Uses neutral, respectful language  
✅ Prefaces with "According to law..."  
✅ Includes legal disclaimer  
✅ Promotes calm, lawful behavior  
✅ Suggests polite, legal questions  
✅ Respects all authorities while explaining rights  

---

## 📊 Confidence Scoring System

The confidence score reflects how well your input matches a legal situation:

| Score | Meaning | Recommendation |
|-------|---------|-----------------|
| **≥80%** | High confidence match | Likely correct situation |
| **60-80%** | Medium confidence | Explore multiple matches |
| **40-60%** | Lower confidence | Try rephrasing input |
| **<40%** | Weak match | Input lacks clarity |

**How it's calculated:**
- All required signals present = 70% base score
- Each optional signal present = +10% bonus (up to 100%)
- Maximum bonus capped at 30%

---

## 🐛 Troubleshooting

### Issue: "No matching legal situations found"

**Solutions:**
1. Check spelling and grammar
2. Use more specific keywords (e.g., "police stopped me" instead of "stopped")
3. Try different language (Hinglish often works well)
4. Add more context to your description

### Issue: Data not loading

**Solutions:**
1. Verify `data/` folder exists with JSON files
2. Check JSON syntax: `python -m json.tool data/keywords.json`
3. Ensure correct file permissions
4. Check console for error messages

### Issue: PyQt5 won't import

**Solutions:**
```bash
pip uninstall PyQt5 -y
pip install PyQt5==5.15.7 PyQt5-sip==12.11.1
```

### Issue: Slow performance

**Solutions:**
1. Close unnecessary programs
2. Reduce window size (less rendering)
3. Check system RAM usage
4. Restart application

---

## 📦 Building Standalone .exe (Windows)

To create a standalone executable:

```bash
# Install PyInstaller (already in requirements)
pip install pyinstaller

# Build .exe
pyinstaller --name=LegalAssist \
    --windowed \
    --icon=icon.ico \
    --add-data="data:data" \
    --add-data="ui:ui" \
    --add-data="engine:engine" \
    main.py

# .exe will be in: dist/LegalAssist/LegalAssist.exe
```

For macOS .app:
```bash
pyinstaller --name=LegalAssist \
    --windowed \
    --osx-bundle-identifier=com.legalassist.app \
    --add-data="data:data" \
    main.py
```

---

## 📚 Legal Coverage (MVP)

### Constitution of India
- Article 19(1)(d): Freedom of Movement
- Article 21: Protection of Life and Personal Liberty

### Indian Penal Code (IPC)
- Section 341: Wrongful Restraint
- Section 342: Wrongful Confinement
- Section 354: Assault with Intent to Outrage Modesty
- Section 504: Intentional Insult with Knowledge of Causing Breach
- Section 506: Criminal Intimidation
- Section 509: Word/Gesture to Insult Modesty of Woman
- Section 420: Cheating

### Code of Criminal Procedure (CrPC)
- Section 41: Arrest Without Warrant
- Section 50: Informing of Grounds of Arrest
- Section 160: Examination by Police Officer
- Section 165: Search Without Warrant

### Information Technology Act
- Section 66: Computer Hacking
- Section 66D: Cheating by Personation

### Juvenile Justice Act
- Protection of Minors During Custody

---

## 🔄 Future Enhancements

- [ ] Case history storage (SQLite)
- [ ] PDF export of guidance
- [ ] Emergency helpline integration
- [ ] Regional language expansion (Tamil, Bengali, Marathi, etc.)
- [ ] Admin panel for JSON editing
- [ ] Mobile app (React Native)
- [ ] Web version (Flask + React)
- [ ] Voice input support
- [ ] Integration with legal aid organizations
- [ ] Real-time law updates

---

## 📖 References & Legal Sources

- Constitution of India (Official Text)
- Indian Penal Code (Official Text)
- Code of Criminal Procedure, 2023
- IT Act, 2000
- Juvenile Justice (Care and Protection of Children) Act, 2015
- NHRC Guidelines on Citizens' Rights
- Supreme Court Judgments (cited in law sections)

---

## 📝 License

This project is created for **educational and awareness purposes only**.

Not licensed under GPL/MIT (custom educational license).

**Use for:**
- Personal legal awareness
- Educational institutions
- NGOs and legal aid organizations
- Government awareness programs

**Restrictions:**
- Not for commercial resale as legal services
- Always include disclaimer
- Don't represent as legal advice

---

## 🤝 Contributing

Contributions welcome!

### How to Contribute:
1. Report bugs (GitHub Issues)
2. Suggest new situations/laws (Discussions)
3. Improve keyword detection
4. Translate to regional languages
5. Enhance UI/UX

**Before contributing:**
- Review legal accuracy with qualified lawyer
- Test with real users
- Maintain ethical guidelines
- Document changes

---

## ⚠️ Important Legal Disclaimer

**LegalAssist is NOT a substitute for professional legal advice.**

This system:
- Provides general legal awareness only
- Does NOT constitute legal advice
- Should NOT be used as a substitute for a lawyer
- Is for educational purposes only
- Does NOT create attorney-client relationship
- Cannot guarantee legal outcomes

**For serious legal matters, always consult a qualified lawyer.**

---

## 👨‍💻 Developer Contact

- **Email:** [Your Email]
- **GitHub:** [Your GitHub]
- **Twitter:** [Your Twitter]

---

## 📞 Emergency Resources

**If you need immediate help:**

- **National Police Complaint Authority (NPCA):** 011-2430-2023
- **National Human Rights Commission (NHRC):** 1800-233-0336
- **Free Legal Aid:** indianlegalaidboard.org
- **Bar Council of India:** bcindia.org

---

**Last Updated:** December 2024  
**Version:** 1.0.0  
**Status:** ✅ Production Ready

---

*"Know Your Rights. Understand The Law."* ⚖️
