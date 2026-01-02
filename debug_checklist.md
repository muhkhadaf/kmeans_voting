# Debugging Checklist: Vote Submission Issue

## Issue
User activated voting period but ratings still not being saved to database.

## Checks Completed
- ✓ Form structure verified - submits to `/submit_vote` with all required fields
- ✓ `submit_vote` route code reviewed - logic appears correct
- ? Voting period status - need to verify it's truly active
- ? Candidates exist - need to verify
- ? Database receiving data - need to check

## Next Steps
1. Verify voting period is active and within time range
2. Verify candidates are set
3. Add debug logging to trace execution
4. Test submission and check Flask terminal output
5. Check browser console for JavaScript errors
