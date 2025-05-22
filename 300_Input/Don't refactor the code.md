---
tags:
  - 🎁Topic/Tech
---

[[ReadItLater]] [[Article]]

# [Don't refactor the code](https://dev.to/katafrakt/dont-refactor-the-code-igk)

This is a piece of advice someone gave me a long time ago. Unfortunately, I don't really remember who, so I cannot properly attribute (although chances are they heard it somewhere too). But I decided to re-share this.

**What is refactoring?** I'm sure we can find multitude of definitions. But with modern software development process it often becomes synonymous with any kind of code changes that do not add, modify or remove features. In other words, a non-product work. In effect it often becomes a blurry term and cause of tension between product stakeholders and the dev team.

Who among us did not hear that on a status meeting: "Yesterday I spent most time refactoring the code around X"? I know I did. No less, I probably said a phrase like that more than once. What does this mean? What did you really do? This is hidden behind "I refactored" term. "I did an important technical work you would not understand" is another way of framing that.

And this is exactly the problem with "refactoring the code". In many cases it means doing a really important work, but it's indistinguishable from almost-slacking-off, like renaming variables for no apparent reason.

And this is what I mean by "don't refactor the code": use different words when talking about things you did, are doing or plan to do. Don't "refactor". Instead try these:

-   I made the code more performant (identified N+1, found inefficient processing of a large amount of data)
    
-   I made the code more open to change (mostly should be justified by prediction that we will be changing this area more often now)
    
-   I made the code more defensive (failing early and with a clear message if run with incorrect arguments - because other teams are using it incorrectly and it leads to a subtle bugs)
    
-   I added the tests for an untested area (good rationale: because it failed few times recently; bad rationale: to increase our arbitrary code coverage metrics)
    
-   I added more logging / instrumentation (so we can understand better what is going on)
    
-   I change the code to meet our new style guide (because we will change it often)
    

Communicating like this is not only makes it easier for others to understand what was changed, but also helps you decide if the change you plan to make really makes a difference. Not being able to hide behind an umbrella "refactoring" term also helps to keep the changes more focused and easier to review for your colleagues.