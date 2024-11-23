# Contribution Guide

## Feature/Task Branch Naming
- Branches for tasks will be created by branching off of the `dev` branch with the following naming convention:  
  **`feature[tasknumber]_simple_details_about_task`**

## Quick Fix Branches
- Branch off `dev` with the following naming convention:  
  **`fix[tasknumber]_simple_details_about_fix`**

## Pull Requests
- Create pull requests from your feature branch to the `dev` branch.
- Assign **one person** as the reviewer and **yourself** as the assignee.
- Handle any merge conflicts on the requester's end by merging down.

## Commit Messages
- Write **detailed messages** that concisely and accurately describe the changes made.
- Must have frequent and incremental **commits** to ensure stability

## Trello Workflow
1. When starting work on a task, move the ticket for the task into **"In Progress"** and attach the branch using the GitHub Power-Up.
2. When creating unit tests, move the ticket into **"Testing"**.
3. When a pull request is created, attach the PR to the ticket using the GitHub Power-Up and move it into **"Code Review"**.
