from askui.models.shared.tools import Tool


class GetTestReportTemplateTool(Tool):
    """
    Get the test report template.
    """

    def __init__(self):
        super().__init__(
            name="get_test_report_template_tool",
            description="""
            Get the test report template.
            It must be used to get the test report template for the test case.
            Helps you to understand how to write the test report for the test case.
            Must be used as first tool to get the test report template.
            """,
        )

    def __call__(self) -> str:
        return """
**Report Structure:**
```markdown
# Test Case: {test_case.test_case_id} - {test_case.title}

## Test Case Description
{test_case.title}

## Pre-conditions
{test_case.pre_action}

## Test Steps

### Step X: [Action Description]
**Action:** [Detailed action performed]
**Expected Result:** [What should happen]
**Actual Result:** [What actually happened]
**Evidence:** 
- screenshot:![Screenshot](./{index + 1}_{test_case.test_case_id}_images/[descriptive_filename].png)
- shell output (if present): 
```bash
{shell_output}
```
**Status:** ✅ PASS / ❌ FAIL / ⚠️ BLOCKED
**Notes:** [Any additional observations or issues]

## Overall Test Result
**Status:** ✅ PASS / ❌ FAIL / ⚠️ BLOCKED
**Execution Time:** [Start] - [End]
**Issues Encountered:** [List any problems]
**Notes:** [Final observations and recommendations]
```

### 4. SCREENSHOT MANAGEMENT
- Save all screenshots in: `{folder_name}/{index + 1}_{test_case.test_case_id}_images/`
- Use descriptive filenames: `01_initial_screen.png`, `02_action_performed.png`, etc.
- Don't forget to add the screenshots to the markdown file.
- Add all screenshots to the markdown file.
- Include screenshots for:
  * Initial state
  * After each significant action
  * Error states or unexpected behavior
  * Final state

Example Step:
```markdown
### Step 1: Open the app menu
**Action:** Clicked on the app menu button located at (100, 100)
**Expected Result:** The app menu should open
**Actual Result:** The app menu opened
**Evidence:** 
- screenshot:![Screenshot](./TestID/01_initial_screen.png)
**Status:** ✅ PASS
```

Example Step 2:
### Step 5: Mute the audio
**Action:** Clicked on the mute button using the volume control tool
**Expected Result:** The audio should be muted
**Actual Result:** The audio was muted according to the mute icon presence.
**Evidence:** 
- screenshot:![Screenshot](./TestID/05_mute_audio.png)
**Status:** ✅ PASS
"""
