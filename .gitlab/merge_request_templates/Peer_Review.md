To Request a Peer Review
========================
 - This merge request should be from your feature branch to the Master branch.  
 - The title of the merge request should contain the ticket number and a REALLY short description.  
 - "Description" -- Provide a brief description of the change.  
 - "Deployment for Testing Instructions" -- Update the instructions for deploying this package change to a non-production environment.  
 - "Testing Plan" -- Briefly describe how this change will be tested.  
 - "Related Projects" -- If this merge is dependent any other project merge, add it under cross-project dependencies
 - "Deployment to Production Instructions" -- Update the instructions for deploying this to production.  These can be updated after testing if needed.  
 - "Approval" -- Upon completion of testing, look up the production approval in the [eis_change_management](https://gitlab.wm.edu/eis_change_management/eis_change_management/issues) project under issues and edit this description to add the issue number next to the "#" below.  If you received multiple approvals, list them all with "Close " in front of each.  
 - "Rollback Plan" -- Update the rollback plan if needed.  
 - Upon submission, the label ~"Peer Review" will be applied.  
 - Be sure to assign the merge request to the developer you would like to review your code.  
 - You can delete any sections not applicable to this project.  
 - You can delete from here up once you have completed the instructions above.  


Description
===========
-- Describe this change. --  


Deployment for Testing Instructions
==================================
```bash
python -m pip install --upgrade --user git+ssh://git@code.wm.edu/IT/software-systems/eispippackages/msgraph.git@test
```


Testing Plan
======================
-- Describe how the change will be tested. --  


Deployment to Production Instructions
==================================
```bash
python -m pip install --upgrade git+ssh://git@code.wm.edu/IT/software-systems/eispippackages/msgraph.git
```


Approval
=============
-- Obtained after testing is complete --  
Approval == Close eis_change_management/eis_change_management#


Rollback Plan 
=============
Revert to the previous version. 


Peer Reviewer
=============
If you see any issues with the points below, submit as a conversation describing your concern.  If this merge request proceeds after a discussion has begun, it must be marked "Resolved".  After a positive peer review and all boxes are checked click the "Merge" button. After the merge completes successfully, re-assign to the developer.

* [ ] Structure
  - Package should follow a pattern of reasonable separation of purpose. Data and logs should not live with code. 
  - Hardcoded values should be placed in external settings files (including email addresses) and referenced. The settings file should be ignored and in it's place a template_settings file should contain only non-secret information. 
  - Avoid DB links and instead use instance specific database connections.

* [ ] Secrets
  - The package should not contain any keys, passwords or usernames. 

* [ ] Sustainability
  - To the extent possible, the package should be able to be re-useable for multiple processes 

* [ ] Good Practices
  - General code quality and good practices.
  - Code should contain a reasonable level of comments describing it's intended purpose/functionality. 
  - Code should have a reasonable amount of exception handling and error logging for troubleshooting issues. 
  - The package should contain a README.md file with information describing how to install and use the package.

* [ ] `setup.py`
  - Package version should be incremented to denote a new version/update to the package.
  - The package url should be up-to-date, denoting where the package can be currently found.
  - The `setup` function call should include a `install_requires` parameter listing the required packages for this package

/label ~"Peer Review"

