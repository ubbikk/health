# Document XML Transform Rules

Your task is to transform medical documents into XML format following these instructions. Transform each document independently, focusing on capturing key clinical information in a structured format.

## Enums and Constants

SPECIALTY = [
    "cardiology",
    "endocrinology",
    "gastroenterology",
    "neurology",
    "pulmonology",
    "rheumatology",
    "nephrology",
    "hematology",
    "immunology",
    "oncology",
    "surgery",
    "orthopedics",
    "urology",
    "gynecology",
    "ophthalmology",
    "dermatology",
    "psychiatry",
    "lab",
    "radiology",
    "general"
]

CATEGORY = [
    "lab_result",
    "consultation",
    "monitoring",
    "imaging",
    "procedure",
    "emergency",
    "screening",
    "followup",
    "therapy",
    "surgery"
]

DIAGNOSIS_STATUS = [
    "active",           # Current acute condition
    "resolved",         # Condition that was treated and resolved
    "suspected",        # Not fully confirmed diagnosis
    "chronic",          # Long-term condition in stable state
    "chronic_active",   # Long-term condition with current symptoms/progression
    "chronic_remission", # Long-term condition currently under control
    "chronic_relapse"   # Long-term condition with new acute phase
]

RESULTS_SEVERITY = [
    "normal",    # All results within reference ranges
    "warning",   # Results outside reference ranges but not critically
    "critical"   # Results requiring immediate attention
]

## Output Format
```xml
<doc>
    <type>Use exact type name from document</type>
    <date>YYYY-MM-DD</date>
    <meta>
        <specialty>value from SPECIALTY</specialty>
        <category>value from CATEGORY</category>
        <urgency>routine|urgent|emergency</urgency>
        <followup>true|false</followup>
        <results_severity>value from RESULTS_SEVERITY</results_severity>
    </meta>
    <diagnoses>
        <diagnosis>
            <condition>Name of condition</condition>
            <status>value from DIAGNOSIS_STATUS</status>
            <date_noted>YYYY-MM-DD</date_noted>
        </diagnosis>
        <!-- Multiple diagnosis elements allowed -->
    </diagnoses>
    <treatments>
        <current>Brief description of ongoing treatment</current>
        <recommended>Brief description of new recommendations</recommended>
    </treatments>
    <summary>
        Concise summary (2-3 sentences) that must:
        - Start with most significant finding/conclusion
        - Include severity context for abnormal results
        - Skip normal findings unless clinically relevant
        - Use original document language
    </summary>
</doc>
```

## Transformation Rules

1. Document Type and Date
   - Use exact document type as written in source
   - Convert dates to ISO format (YYYY-MM-DD)

2. Meta Information
   - Assign most relevant specialty based on document content
   - Choose appropriate category based on document purpose
   - Set results_severity for all diagnostic documents
   - Mark urgency as "urgent" or "emergency" only if explicitly stated

3. Diagnoses Section
   - Include only when diagnoses are explicitly stated or modified
   - Use most specific status from DIAGNOSIS_STATUS
   - Include date when diagnosis was noted in current document
   - List all diagnoses mentioned, both new and confirmed existing ones

4. Treatments Section
   - Include only when treatments are mentioned
   - In 'current': list only explicitly mentioned ongoing treatments
   - In 'recommended': list new prescriptions and recommendations
   - Keep descriptions brief and focused on key points

5. Summary Creation
   - Maximum 2-3 sentences unless critical findings present
   - First sentence must state most important finding/conclusion
   - For lab results: start with abnormal findings and their severity
   - For consultations: start with main diagnosis/conclusion
   - Skip normal results unless they're important in clinical context
   - Maintain original document language
   - Include quantitative values for significant findings

6. General Rules
   - Skip institutional/patient identifying data
   - Keep original document language
   - Include quantitative values for significant findings
   - Don't include detailed reference ranges unless critically relevant
7. Output Format Rules
- Output ONLY XML without any additional text or explanations
- Skip institutional/patient identifying data
- Keep original document language
- Include quantitative values for significant findings
- Don't include detailed reference ranges unless critically relevant

## Examples

Example 1 - Lab Result:
```xml
<doc>
    <type>Результати аналізу крові</type>
    <date>2024-01-15</date>
    <meta>
        <specialty>lab</specialty>
        <category>lab_result</category>
        <urgency>routine</urgency>
        <followup>false</followup>
        <results_severity>warning</results_severity>
    </meta>
    <summary>
        Виявлено підвищений рівень лейкоцитів 12.3×10⁹/л (норма 4-9×10⁹/л). Інші показники загального аналізу крові в межах норми.
    </summary>
</doc>
```

Example 2 - Consultation:
```xml
<doc>
    <type>Консультація кардіолога</type>
    <date>2024-02-01</date>
    <meta>
        <specialty>cardiology</specialty>
        <category>consultation</category>
        <urgency>routine</urgency>
        <followup>true</followup>
        <results_severity>normal</results_severity>
    </meta>
    <diagnoses>
        <diagnosis>
            <condition>Гіпертонічна хвороба</condition>
            <status>chronic_remission</status>
            <date_noted>2024-02-01</date_noted>
        </diagnosis>
    </diagnoses>
    <treatments>
        <current>Бісопролол 5мг/день</current>
        <recommended>Продовжити поточне лікування, контроль АТ щоденно</recommended>
    </treatments>
    <summary>
        Стан стабільний, АТ контрольований на поточній терапії (середні показники 135/85). Рекомендовано продовжити прийом бісопрололу та щоденний контроль АТ.
    </summary>
</doc>
```


Output ONLY XML without any additional text or explanations!