# 🚀 LegalAssist - Quick Start Guide

## Installation (5 minutes)

### Step 1: Requirements
- **Python 3.8+** (download from python.org)
- **pip** (comes with Python)

Verify installation:
```bash
python --version
pip --version
```

### Step 2: Project Setup

```bash
# Download project files
# Extract to folder: C:\LegalAssist (or any location)

cd LegalAssist

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- **PyQt5** (GUI framework)
- **python-hindi** (language support)
- **pyinstaller** (for building .exe)

### Step 4: Run Application

```bash
python main.py
```

**Window should open in 3-5 seconds!**

---

## Project Directory Structure

```
legalassist/
│
├── 📄 main.py                    ← RUN THIS FILE
├── 📄 requirements.txt           ← Dependencies
├── 📄 README.md                  ← Full documentation
├── 📄 QUICKSTART.md              ← This file
│
├── 📁 data/                      ← JSON data files
│   ├── keywords.json             (342 keywords, 17 categories)
│   ├── situations.json           (9 legal situations)
│   └── laws.json                 (16 laws, full references)
│
├── 📁 engine/                    ← Core matching logic
│   ├── normalizer.py             (text preprocessing)
│   ├── matcher.py                (keyword matching)
│   └── resolver.py               (confidence scoring)
│
├── 📁 ui/                        ← User interface
│   ├── styles.py                 (PyQt5 styling)
│   └── components.py             (reusable widgets)
│
├── 📁 utils/                     ← Helper utilities
│   └── translator.py             (Hindi/English conversion)
│
└── 📁 venv/                      ← Virtual environment (created after setup)
```

---

## Usage Examples

### Example 1: Police Harassment
```
Input: "police ne roka aur parents ko call karne ko bola"
Output:
  - Situation: Police Harassment / Wrongful Detention
  - Confidence: 95%
  - Laws: Article 19(1)(d), Article 21, IPC 341
```

### Example 2: Verbal Abuse
```
Input: "cop used bad language and threatened me"
Output:
  - Situation: Police Verbal Harassment
  - Confidence: 88%
  - Laws: IPC 504, IPC 506, Article 21
```

### Example 3: Body Search
```
Input: "policeman searched me without asking permission"
Output:
  - Situation: Police Privacy Violation / Illegal Search
  - Confidence: 92%
  - Laws: IPC 354, CRPC 165, Article 21
```

---

## Troubleshooting

### Error: "No module named 'PyQt5'"
```bash
pip uninstall PyQt5 -y
pip install PyQt5==5.15.7 PyQt5-sip==12.11.1
```

### Error: "data/keywords.json not found"
- Verify `data/` folder exists in same directory as `main.py`
- Check file names are correct (case-sensitive on Linux/Mac)

### Application runs slowly
- Close other programs
- Ensure you have 2+ GB RAM available
- Restart application

### JSON syntax error when editing
```bash
# Validate JSON files:
python -m json.tool data/keywords.json
python -m json.tool data/situations.json
python -m json.tool data/laws.json
```

---

## Building Standalone .exe (Windows)

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Create .exe
```bash
pyinstaller \
  --name=LegalAssist \
  --windowed \
  --add-data="data;data" \
  --add-data="engine;engine" \
  --add-data="ui;ui" \
  main.py
```

### Step 3: Find Your .exe
```
dist/LegalAssist/LegalAssist.exe
```

You can now share this standalone .exe with others!

---

## Testing the System

### Test Case 1: Basic Match
```
Input: "police stopped me"
Expected: Police Wrongful Detention situation found
Confidence: Should be >70%
```

### Test Case 2: Hinglish Mix
```
Input: "roka aur badmashi ki"
Expected: Police harassment detected
```

### Test Case 3: Hindi Text
```
Input: "पुलिस ने मुझे रोका"
Expected: Police stop detected
```

### Test Case 4: Low Confidence
```
Input: "something happened"
Expected: "No matching situations found" or low confidence matches
```

---

## Key Files Explained

### main.py
- PyQt5 application entry point
- Handles UI, user interaction, result display
- Loads data files and initializes matching engine

### engine/matcher.py
- Core matching logic
- Orchestrates: normalize → detect signals → match situations → retrieve laws
- Entry point: `process_query(user_input)`

### engine/normalizer.py
- Converts user text to lowercase
- Removes punctuation
- Applies Hinglish-to-English translation
- Detects language mix (English/Hindi/Hinglish)

### engine/resolver.py
- Calculates confidence scores (0-100%)
- Ranks situations by match quality
- Handles low-confidence scenarios (returns top 3 matches)

### data/keywords.json
- 17 semantic signal categories
- ~342 keywords across English, Hindi, Hinglish
- Globally reusable, situation-agnostic

### data/situations.json
- 9 pre-defined legal situations
- Each specifies required and optional signals
- Maps to applicable laws

### data/laws.json
- 16 Indian laws with full references
- Constitution, IPC, CrPC, IT Act, Juvenile Justice Act
- Includes explanations, key points, penalties

---

## Customizing LegalAssist

### Add a New Situation

1. **Open situations.json**
2. **Add new entry** (copy existing, modify):
   ```json
   "WORKPLACE_HARASSMENT": {
     "id": "WH001",
     "name": "Workplace Harassment",
     "required_signals": ["EMPLOYER", "HARASSMENT_VERBAL"],
     "optional_signals": ["THREAT_INTIMIDATION"],
     "law_ids": ["LABOR_ACT_SECTION"],
     "severity": "medium"
   }
   ```

3. **Add keywords** (if needed to keywords.json):
   ```json
   "EMPLOYER": {
     "keywords": ["boss", "manager", "HR", "employer"],
     "hinglish": ["malik", "manager"],
     "hindi": ["मालिक", "प्रबंधक"],
     "confidence_weight": 0.9
   }
   ```

4. **Add laws** (if needed to laws.json):
   ```json
   "LABOR_ACT_SECTION": {
     "id": "LABOR_ACT_SECTION",
     "type": "Labor Law",
     "section": "Section X",
     "title": "Law Title",
     "explanation": "Clear explanation...",
     "key_points": ["Point 1"],
     "what_you_can_ask": ["Question 1"],
     "punishment_if_violated": "..."
   }
   ```

5. **Restart application** - changes load automatically!

### Edit Existing Law

1. Open `data/laws.json`
2. Find law by ID (e.g., "IPC_341")
3. Modify explanation, key_points, punishment_if_violated
4. Save and restart

### Add Hindi/Hinglish Keywords

For any category in keywords.json:
```json
"AUTHORITY_POLICE": {
  "keywords": ["police", "cop"],
  "hinglish": ["police", "cop", "thana"],
  "hindi": ["पुलिस", "सिपाही"],
  "confidence_weight": 1.0
}
```

---

## Performance Tips

- **First run:** Application loads JSON into memory (fast subsequent runs)
- **Large input:** Can handle 500+ character descriptions
- **Multiple matches:** Returns top 3, all >0% confidence
- **Memory:** Uses ~150-200 MB RAM (acceptable for desktop app)

---

## Safety Features

✅ **No internet communication** (all processing local)  
✅ **No data storage** (queries not saved unless you modify code)  
✅ **No external APIs** (completely standalone)  
✅ **Open source** (review code for security)  
✅ **Offline capable** (works without internet)  

---

## Common Questions

### Q: Can I use this as legal advice?
**A:** No. LegalAssist is educational only. Always consult a lawyer for legal matters.

### Q: Will this help me in court?
**A:** No. This explains laws. Legal representation requires a qualified lawyer.

### Q: Can I share .exe with others?
**A:** Yes! Build standalone .exe (instructions above) and distribute freely.

### Q: How often are laws updated?
**A:** Update JSON files as laws change. Version 1.0 reflects laws as of Dec 2024.

### Q: Can I add regional laws (state-specific)?
**A:** Yes! Add to situations.json and laws.json. System will match automatically.

### Q: How do I expand keyword matching?
**A:** Edit keywords.json with new categories and keywords. No code changes needed!

---

## Support & Resources

- **Issues:** Check GitHub Issues
- **Suggestions:** GitHub Discussions
- **Legal Help:** Refer user to qualified lawyer
- **AI Help:** Consult legal aid organizations

---

## Version Info

- **Version:** 1.0.0
- **Release Date:** December 2024
- **Python:** 3.8+
- **Status:** Production Ready ✅

---

## Next Steps

1. ✅ Run `python main.py`
2. 📝 Test with examples above
3. 🔧 Customize with your own situations/laws
4. 📦 Build standalone .exe when ready
5. 📢 Share with others who benefit from legal awareness

---

**Happy Learning! ⚖️**

"Know Your Rights. Understand The Law."
