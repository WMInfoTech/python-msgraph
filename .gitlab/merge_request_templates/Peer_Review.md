To Request a Peer Review
========================

 - The title of the merge request should contain the ticket number and ticket description.  
 - Provide a brief description of the package or change.  
 - Upon submission, the label ~"Peer Review" will be applied.  
 - Be sure to assign the merge request to the developer you would like to review your code.  
 - This merge request should be from your feature branch to the master branch.  
 - Complete the deployment for testing instructions with specific commands as needed.  
 - You can delete from here up once you have completed the instructions above.  

Description
===========
Provide a description of the change to the package here. 

Deployment for Testing Instructions
==================================
```python
python -m pip install --upgrade --user git+ssh://git@code.wm.edu/IT/software-systems/eispippackages/msgraph.git@test
```

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

/label ~"Peer Review"
