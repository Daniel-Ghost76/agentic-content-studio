# Batch 16: Videos 241-242

## Video 241: How to Create an AI Email Agent with n8n (No Code, Step-by-Step Tutorial) (21/09/24)
**Words:** 5300 | **Chunks:** 2

**Hook:** all right so today I'm going to be walking through step by step how to build a super simple email AI agent

**Hook Type:** Demonstration

**Credential Drop:** 5 years of coding experience um yeah obviously that's a joke because that's kind of the whole point of this video and these low code no code tools so we're going to be building three separate workflows today

**Signature Phrases:**
- "you guys"
- "here we go"
- "let me hit you with"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"
- "let's not waste any time"
- "here we go"
- "what's really cool"

**Transitions:**
- so let's get straight into this one
- hey Phil just checking in to see what's up best Nate super simple email but just wanted to give you guys a quick demo of that okay let's get into actually building this now so the resources needed for this video naden that is the software we're going to be using to to build this um agent
- let me just show you what my contact data looks like so um these are all of my best friends pretty much I've got their email addresses here obviously fake email add addresses besides this one is one of mine so we're going to be sending it to Phil dumpy and that's how it knows to send it to this email address here
- all right so let's just go in here hey Phil just checking in to see what's up best Nate super simple email but just wanted to give you guys a quick demo of that okay let's get into actually building this now so the resources needed for this video naden that is the software we're going to be using to to build this um agent
- so we've got pine cone we've got the send email now we're going to actually make the agent so first up again we have to build a we have to put a trigger we're going to use on chat message this time because we want to trigger the agent or trigger the workflow by talking to it
- so this is what we need to do for now
- we're just going to touch tool and chat model for today so chat model same thing open AI connect it we're going to grab 40 especially for one that's going to be talking to us and thinking tool we're going to call an n8n workflow this is obviously the one that we just made the tool that's a send email just want to keep everything organized here
- Source um database the workflow we can Define from a list um you can also do it by ID but you'd have to grab that URL thing so the list is easier because we have the send email right here field to return response so that's when we set the response field earlier to sent and let's see is there anything else that we need to do on this one
- specify input schema yeah that's what we need to do we want to Define below and this is like the schema that this tool is going to be using so what we need to do save that real quick we need to go back to our send email tool we need to make sure that the schema is the same from right here because this is what we gave this tool
- oh can't forget to do the embedding otherwise it wouldn't know how to figure out what's a name what's an email address that sort of thing so again make sure it's three small because that's how we set up our Vector store and then we're just going to save that okay so going to test this out now hopefully it doesn't air but if it does we can sort of go into how you can find out where it's airing and how to fix that
- so let's try this so again send an email to Bill duny asking if he wants to get lunch seems there's an issue with sending the email would you like to try again later okay so let's see what happened we can see it AED at the send email tool we're going to go to all executions to figure out what happened
- okay something cool that you can do is grab a screenshot of this workflow copy that we're going to go back into chat we're going to give it this picture and say please prompt this agent um include the parameters for the email tool as well as overall context background and instructions okay so prompting is super super important this definitely is not the way you'd want to do it when you're really building out a complicated agent but for now this should work
- let's see if this works we're just going to grab from here up well okay so it's got context background instructions it included the parameters here for the email tool so let's try this again right now I just thought it was a helpful assistant which it is but it didn't have all of this instructions and also one thing I like to do at the end is um sign off the email from Nate because it knows the sender name is usually just for when it pops up right here to say like it's from Nate but sometimes down here it would say in Brackets like sender name or something so it's nice to sort of specify that so we got that saved in here let's try that again send an email to Phil dumpy asking if he wants to get launch and we just hope that he says yes I've sent an email to Phil dumpy inviting him to launch is there anything else I can assist you with okay perfect inbox launch invitation hey Phil would you like to get lunch sometime best Nate
- so that is just a very very basic one it's got one tool we didn't even give it a Windows memory buffer which is just how you can continuously chat it'll it'll keep history of past messages that you've sent and it's going to be able to know to work off those but that's just a very basic one and it's it's really good to get in here and play around with n8n it's going to give you a great idea of like I said the triggers different nodes as you can see there's so many Integrations like if we just go to you know Gmail you've got all these different things and you can build an agent that strictly can do everything for you that you might need to do in Gmail like an inbox management agent

**CTA / Outro:** "so that is just a very very basic one it's got one tool we didn't even give it a Windows memory buffer which is just how you can continuously chat it'll it'll keep history of past messages that you've sent and it's going to be able to know to work off those but that's just a very very basic one and it's it's really good to get in here and play around with n8n it's going to give you a great idea of like I said the triggers different nodes as you can see there's so many Integrations like if we just go to you know Gmail you've got all these different things and you can build an agent that strictly can do everything for you that you might need to do in Gmail like an inbox management agent"

**Vocabulary:**
- super simple
- Vector database
- large language model
- contact information
- Google Docs
- pine cone
- API Keys
- client ID
- client secret
- Google Cloud account
- send email
- tool
- schema
- prompting
- workflow
- Vector database
- pine cone

**Analogies:** NOT FOUND

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** "5 years of coding experience um yeah obviously that's a joke because that's kind of the whole point of this video and these low code no code tools"

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] so let's get straight into this one we just wanted to start off here with a quick demo of what the agent actually looks like and what it's going to do
- [slow] all right so today I'm going to be walking through step by step how to build a super simple email AI agent if you know anything about agents you know that they can get super complex as you give them access to more tools and expose them to different scenarios so I just wanted to keep this first one super simple just to give everyone a good understanding of what agents are capable of and how you connect them to Tools in order to do what you want them to do to automate workflows basically

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"
- "you guys"
- "those of you"
- "if you've been with me"

**Frameworks:** NOT FOUND

---

## Video 242: How I Wish Someone Explained AI Agents To Me (as a beginner) (20/09/24)
**Words:** 2421 | **Chunks:** 1

**Hook:** so AI agents there's so much information out there it can be overwhelming trying to learn about them so I wanted to come in here and break it down simply just the way that I wish someone would have explained it to me when I first started learning about them

**Hook Type:** Problem-Statement

**Credential Drop:** NOT FOUND

**Signature Phrases:**
- "you guys"
- "here we go"
- "what's really cool"
- "let me hit you with"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"

**Transitions:**
- so I wanted to start off by touching on the golden opportunity that I see and that a lot of people are starting to see in um the AI agent space
- so here's kind of what we did in the past right
- moving on to why you should care about agents and why you should care about this opportunity
- that could be like a 30- minute topic there

**CTA / Outro:** "if it sounds like you and you want to dive into the AI agent space or AI automations in general definitely check out some videos in the future"

**Vocabulary:**
- golden opportunity
- skeptical
- search interest
- perfect memory
- exact instructions
- fraction of hiring an actual human being
- advanced ai models
- pluses
- upsell
- prompting

**Analogies:**
- "imagine having an employee who has Perfect Memory follows exact instructions doesn't sleep and costs a fraction of hiring an actual human being"
- "think of it like they're going to be working 24/7 even if it's something as simple as customer support"
- "it's just going to cost a fraction of hiring an actual human so um yeah it sounds too good to be true almost"
- "like all of that's removed pretty much it'll do that all of that automatically for you"
- "The Entity is just an AI agent with the ability to reason use logic to make decisions and access the tools that you give them in order to do exactly what it is that you're prompting them to do"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:**
- [time_references] 20/09/24
- [named_tools] chat gbt
- [named_tools] claw
- [named_tools] n8n

**Vulnerability:** "I was definitely a little skeptical um about the hype"

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] so I wanted to start off by touching on the golden opportunity that I see and that a lot of people are starting to see in um the AI agent space
- [slow] so here's kind of what we did in the past right
- [slow] moving on to why you should care about agents and why you should care about this opportunity

**Audience Language:** "you guys"

**Frameworks:**
- "first things first what exactly are AI agents simply put um an AI agent is like having an employee who has Perfect Memory follows exact instructions doesn't sleep and costs a fraction of hiring an actual human being"

---

