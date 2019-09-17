To Request a Production Release
===============================
 - The title line should contain the EIS ticket number and a description of the project or change. 
 - Enter a description of the change below. 
 - Complete the deployment to production instructions with specific commands as needed.  
 - Look up the Feature -> Test merge request number and enter it next to the "!" below. 
 - Enter a short description of how the change was tested.  
 - Look up the production approval in the eis_change_management project under issues and enter the issue number next to the "#" below. 
 - Upon submission the ~"Stage for Production" label will be applied. 

Description 
===========
Provide a description of the change to the package here. 

Deployment to Production Instructions
==================================
```python
python -m pip install --upgrade git+ssh://git@code.wm.edu/IT/software-systems/eispippackages/msgraph.git  
```

Approval 
========
Approval == Close eis_change_management/eis_change_management#  

Testing 
=======
Feature -> Test Merge Request == !  

Please provide a description of how this change was tested. 

Rollback Plan 
=============
Revert to the previous release. 

Production Release Review
=========================
Please verify and check the box for each item below. If any items below are not satisfied, please comment below and submit as a discussion to the developer. If everything meets the requirements, merge and deploy. 

* [ ] Ticket Number
  - Does the title of the merge request contain a ticket number?

* [ ] Production Approval
  -  Does the request contain a production approval from a user or a qualified internal approver?

* [ ] Description
  - A description of the change has been included. 

*  [ ] Testing
  - Is the Feature -> Test Merge Request linked above?
  - Is a description of how the testing was performed included.

* [ ] Rollback Plan
  - Does the request contain a rollback plan. 


/label ~"Stage for Production"
