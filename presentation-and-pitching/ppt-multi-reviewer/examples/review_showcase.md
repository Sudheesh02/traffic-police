# Example: How the 3 Reviewers Transform a Slide

## Input Slide (Bad: AI Slop, Hyphens, Buzzwords, Stiff English)
```markdown
### Slide: Decarbonization Paradigm
- Our revolutionary architecture—powered by cutting-edge AI—seamlessly leverages synergistic circularity paradigms
- By meticulously analyzing multifaceted metallurgical parameters, it empowers furnace operators to optimize scrap
- Specific carbon footprint is significantly mitigated—a true testament to our holistic vision
```

---

## The 3 Reviewers In Action

### Reviewer 1: The Skeptical Judge
> "I read this and have no idea what your software actually does. What furnace? What scrap? 'Seamlessly leverages synergistic circularity paradigms' makes me want to close the tab. Give me one sentence on the problem, one sentence on what your code did, and the real number."

### Reviewer 2: The Grounded Fact & Code Checker
> "You made zero technical claims. Looking at the codebase in `jsl_carbon_engine/core/carbon_calculator.py`, your engine calculates Scope 1 and Scope 2 emissions, and checks copper tramp thresholds for grade J304. Put the actual number: 4.17 tCO2/t reduced to 1.83 tCO2/t, and state the 1.6 ms response time."

### Reviewer 3: The Anti-AI & Human Voice Auditor
> "This slide has every AI cliché in the book: 'revolutionary', 'seamlessly leverages', 'meticulously', 'empowers', 'testament', 'holistic'. Also, you used em-dashes and hyphens everywhere. Throw all of that away and write it like a human engineer talking to another human."

---

## Output (Polished Winning Slide)

```markdown
### Slide: Cutting Steel Emissions Without Cracking the Slabs
> **Key Takeaway**: Increasing scrap is the fastest way to cut furnace emissions, but too much scrap introduces copper that destroys the steel. We calculate the exact safe limit in 1.6 milliseconds.

#### 1. What Judges Need to Know
* **The Furnace Problem**: Operators want to use recycled scrap to cut carbon, but excess copper causes catastrophic surface cracking during hot rolling.
* **Our Solution**: A real-time mass-balance engine that checks chemical ceilings every time an operator adjusts a scrap slider.

#### 2. Grounded Proof from Code
* [ Carbon Footprint: 4.17 -> 1.83 tCO2/t (-56% drop) ]
* [ Safety Ceiling: Copper capped at 0.40% for Grade J304 ]
* [ Calculation Speed: 1.6 ms response time ]

#### 3. 30-Second Spoken Pitch
"Using scrap cuts carbon fast, but push it too far and copper ruins the steel. Our engine calculates the exact chemical limit live on the floor. Operators get 56% lower emissions without risking cracked slabs."
```
