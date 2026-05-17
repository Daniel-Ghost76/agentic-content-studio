# Batch 15: Videos 225-240

## Video 225: The Best Way to Give AI Agents Tools in n8n (09/11/24)
**Words:** 4293 | **Chunks:** 1

**Hook:** so today I wanted to come in here and talk about the most powerful AI agent Tools in nadn

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
- so here's the old method
- so this new method like I said
- so now we're in the Gmail node that actually sends the email as you can see
- so let's get into just setting up this function this shouldn't take too long it's really really simple if you have used Excel before it's pretty much the same way you sort of do an Excel formula a simple Excel formula not something like a crazy V lookup but so there's different parameters in the from Ai node um
- so we're going to be creating an event first um sync up the calendar and now we have start time end time obviously we need that information for a calendar event and then we just want to add um a summary because that's going to be be the title that comes through in in Google Calendar so if you guys watch my personal assistant video personal assistant 2.0 you probably noticed that I used some of these tools to help the calendar agent or the email agent
- so let's turn green Perfect all right

**CTA / Outro:** "that is all for now so thanks guys"

**Vocabulary:**
- AI agents
- workflows
- node
- parameters
- query
- automation
- function
- tool
- email
- send email

**Analogies:** "think of it like you're asking Siri could you send a text to Mom saying hi I miss you um that way Siri knows who mom is Siri knows what the text is going to say all that kind of stuff"

**Curiosity Gaps:**
- "so now we just have the a AI smart enough to figure out what needs to go where so we'll chat with this guy and make sure it's working let's say can you create an event from 2: p.m. to 400 p.m. called or not called"
- "let's see if we just leave it as CC um and see if it understands if I just say can you copy blank so test out the email tool"
- "so yeah hopefully you guys can see already how quick that was and how easy that was to set up a tool that does something um very intelligently I guess is a good word to say"

**Specificity:**
- [dollars] NOT FOUND
- [percentages] NOT FOUND
- [subscriber_counts] 1,000 members
- [time_references] 09/11/24
- [named_tools] nadn
- [named_tools] Gmail
- [named_tools] Airtable
- [named_tools] Telegram
- [named_tools] Outlook
- [named_tools] Slack

**Vulnerability:** "NONE FOUND"

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] discussing the new method and its benefits, around 1:30-2:00
- [slow] explaining the old method in detail, around 0:45-1:00

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"

**Frameworks:**
- "so here's the old method let's say for example we're having this AI agent send emails for us as we talk to it so we talk to it and then the agent figures out what it needs to do and then it's going to send off the query to the send email tool which is actually a workflow that we've built within nadn"
- "so now we have this new method where the agent can just send it to one tool it doesn't leave it it doesn't go to a different workflow it stays in this workflow and this node right here is able to figure out who it's going to the subject and um what the message is going to say"

---

## Video 226: AI Personal Assistant 2.0 | This Agent Calls Other Agents (No Code) in n8n (06/11/24)
**Words:** 6347 | **Chunks:** 2

**Hook:** so I said can you schedule a meeting for tomorrow with Michael Scott at noon and then can you email him to confirm if that works so we're going to fire that off we'll see it take place real quick

**Hook Type:** Demonstration

**Credential Drop:** NONE FOUND

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
- so I said
- looks like the email just got sent looks like the calendar event just got made and now it's going to respond to us
- now switching over to the new version instead of giving the agent access to tools we gave this agent access to four different agents
- let's hop into a first live example where we'll be using the calendar agent so real quick I'll open up the calendar agent workflow as you can see this agent is being called by the larger agent so the trigger is when called by another workflow this agent all it has to do is understand the incoming query and then figure out which of the three tools it needs to use
- so we're going to hit test workflow on this main agent so that the telegram trigger is listening for a telegram message I'm going to pull up telegram paste in this message real quick that says you create a calendar event with Michael Scott for tomorrow at 600 p.m. for dinner we'll fire this off
- so let's check our calendar as you can see right here tomorrow 600 p.m. we have dinner with Michael Scott and if we click into here we can see that he and fact was invited Michael Scott was one of my emails so this is the email that it sent off to so that's the proof that this agent is working let's go back into the agent click on the execution and make sure that it actually did do exactly what we said
- so I wanted to hop into the editor real quick and explain this dollar sign from AI thing in more detail so that for the rest of the nodes and the Agents that we're testing out it's all going to make more sense
- same format in the sense that it's getting called by the agent so it's triggered like that
- for the first one let's try just saying can you find out some recent news about open AI
- let me show you real quick I used this one in a in the previous video with my personal AI assistant but let's say you had a ton of projects in here and you had notes and you had different statuses you could also do this with something um you know in something like air table or another sort of database system but just using sheets for the sake of the video
- let me type in a few things and we can see how it's coming through all right so I just hit test workflow the telegram trigger is waiting for us to talk to it

**CTA / Outro:** "I know that these four agents weren't super complex as far as the tools that they had access to but you can tell that they're very efficient at sort of delegating out the tasks to the specific tool but the point to take away here is how easy it is to connect an agent to another agent and you know sort of give the bigger agent multiple agents to run through I would say the best rule of thumb is to never give an agent more than like 10 tools would probably be too many as far as it's going to get confused with the prompting and with the flow of how it should be operating but those were the four main agents that we gave this personal assistant"

**Vocabulary:**
- personal assistant
- AI agent
- telegram trigger
- calendar event
- email agent
- projects agent
- research agent
- personal AI assistant
- agent calls other agents
- no code
- calendar agent
- email agent
- research agent
- projects agent
- knowledge base

**Analogies:**
- "it's a lot lot smarter than it used to be"
- "it's super cool that you can sort of bake in like an open AI node within each parameter it's super cool"
- "let me hit you with this one is going to be the email agent so let's hop into this workflow real quick same thing we're calling this agent from another agent so that's why the trigger is here and in this case we're only giving it send email and get email messages"
- "it's going to figure out okay from that query we're going to find the email address and then that's how we're going to fill in the two we're going to we're going to figure out what the message is going to say and then we're going to make a subject and put it here and then finally we're going to actually make the email message and put it in right here email body which is the body message of the email"
- "let's go check our email and see what that one looks like okay that email just came through the subject is project status update hi Nate I hope this message finds you well I wanted to check in and see how the project is coming along could you please provide an update at your earliest convenience thank you best regards Nate"
- "super cool way to get emails quickly summarized from a specific person all right moving on to the third agent that this personal assistant has access to is the research agent let's take a look at what this one is doing same format in the sense that it's getting called by the agent so it's triggered like that the research agent we gave it a very brief prompt basically just saying your research agent you have Wikipedia Hacker News and Sur API to answer the question first search Wikipedia if you can't find it there then look through Hacker News and then if you can't find it there use Sur API so that's just sort of the flow that we wanted to go through"
- "let's see which tool that this one end up using hopefully Sur API but maybe even just Wikipedia again okay so this one actually used a combination of Wikipedia and Hacker News so super cool that it's not going to be blowing through your credits with ins Ser API cuz that can get a little pricey but as of now I just asked three questions and it only used the other two tools so that's super encouraging and cool to see that it is able to figure out how to get your questions answered"
- "let me type in a few things and we can see how it's coming through all right so I just hit test workflow the telegram trigger is waiting for us to talk to it I'm asking what is our policy on health and safety and data privacy so we'll send that off it's going to hit the knowledge base and then it will return us a nice clean answer um let's actually just pull up the document real quick and then we just got our answer from telegram"
- "as you can see our payment terms are that all payments are due upon completion of services we accept cash credit cards blah blah blah for an oral change we charge 35 for standard and 65 for synthetic so as you can see 35 and 65 and then payment terms cash credit and approved financing options um yeah so that seems to be feeding through correctly"
- "8 times um 451 and see what we get there it should be oh I didn't test it we'll test it so now it's going to be running that prompt it will hit the calculator and it's going to say the result of 8 * 451 is 368 so um that's obviously just how the calculator tool works but that's in case you had a prompt where um you wanted to do a calculation within maybe sending a query so that's why we always include the calculator"
- "honestly that's not even true I haven't even fully updated this prompt and it's still working really well"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** "I saw a video from AI Workshop subar hey if you're seeing this keep up the great work but he showcased these new tools that you can give agents that are much much stronger than they used to be"

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] "so I said can you schedule a meeting for tomorrow with Michael Scott at noon and then can you email him to confirm if that works so we're going to fire that off we'll see it take place real quick"
- [accelerate] "looks like the email just got sent looks like the calendar event just got made and now it's going to respond to us the meeting with Michael Scott has been successfully scheduled for tomorrow at noon additionally an email has been sent to him to confirm if that time works"
- [accelerate] "so we're going to hit test workflow on this main agent so that the telegram trigger is listening for a telegram message I'm going to pull up telegram paste in this message real quick that says you create a calendar event with Michael Scott for tomorrow at 600 p.m. for dinner we'll fire this off"
- [accelerate] "so let's check our calendar as you can see right here tomorrow 600 p.m. we have dinner with Michael Scott and if we click into here we can see that he and fact was invited Michael Scott was one of my emails so this is the email that it sent off to so that's the proof that this agent is working let's go back into the agent click on the execution and make sure that it actually did do exactly what we said"
- [accelerate] "so I wanted to hop into the editor real quick and explain this dollar sign from AI thing in more detail so that for the rest of the nodes and the Agents that we're testing out it's all going to make more sense"
- [slow] "so I said can you schedule a meeting for tomorrow with Michael Scott at noon and then can you email him to confirm if that works so we're going to fire that off we'll see it take place real quick it just got Michael Scott's email information from the contact database now it's going to go back to the agent and then the agent is going to figure out which agent to send it to as you can see it's hitting the calendar agent as well as the email agent looks like the email just got sent looks like the calendar event just got made"
- [slow] "now switching over to the new version instead of giving the agent access to tools we gave this agent access to four different agents it has email agent which has actions within email calendar agent which has actions within calendar and the same thing for a research agent and a projects agent this is a lot more powerful and a lot more scalable because once the agent gets the incoming message from our telegram trigger rather than it figuring out which tool it needs to go to and passing a ton of information between each step it's just going to be figuring out okay if I need to do email I'm just going to send it to the email agent and the agent's going to take care of it same thing with the other agents"
- [slow] "so let's check our calendar as you can see right here tomorrow 600 p.m. we have dinner with Michael Scott and if we click into here we can see that he and fact was invited Michael Scott was one of my emails so this is the email that it sent off to so that's the proof that this agent is working let's go back into the agent click on the execution and make sure that it actually did do exactly what we said"

**Audience Language:**
- "you guys"
- "those of you"
- "if you've been with me"
- "you guys"
- "those of you"
- "if you've been with me"

**Frameworks:**
- "the point to take away here is how easy it is to connect an agent to another agent and you know sort of give the bigger agent multiple agents to run through I would say the best rule of thumb is to never give an agent more than like 10 tools would probably be too many as far as it's going to get confused with the prompting and with the flow of how it should be operating but those were the four main agents that we gave this personal assistant"
- "let me type in a few things and we can see how it's coming through all right so I just hit test workflow the telegram trigger is waiting for us to talk to it I'm asking what is our policy on health and safety and data privacy so we'll send that off it's going to hit the knowledge base and then it will return us a nice clean answer um let's actually just pull up the document real quick and then we just got our answer from telegram"
- "as you can see our payment terms are that all payments are due upon completion of services we accept cash credit cards blah blah blah for an oral change we charge 35 for standard and 65 for synthetic so as you can see 35 and 65 and then payment terms cash credit and approved financing options um yeah so that seems to be feeding through correctly"
- "8 times um 451 and see what we get there it should be oh I didn't test it we'll test it so now it's going to be running that prompt it will hit the calculator and it's going to say the result of 8 * 451 is 368 so um that's obviously just how the calculator tool works but that's in case you had a prompt where um you wanted to do a calculation within maybe sending a query so that's why we always include the calculator"
- "honestly that's not even true I haven't even fully updated this prompt and it's still working really well"

---

## Video 227: n8n AI Agent Masterclass | AI Nodes Made Simple (04/11/24)
**Words:** 11187 | **Chunks:** 3

**Hook:** all right everyone welcome to the nadn AI agents Master Class

**Hook Type:** Personal-Moment

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
- "you guys"
- "here we go"
- "let me hit you with"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"
- "you guys"
- "let me hit you with"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"

**Transitions:**
- so for example a conversational agent could gather information from a user pass it to a planning and execute agent
- now I wanted to talk about JavaScript variables and functions within NN because this is something that's super important to understand
- okay now let's break down what we're seeing here
- so this is the prompt for the main instruction or the question that the a agent is going to respond to so this is the direct command that that the agent is expected to look through and act on
- so think of this as like you know giving it the personality and the job description down here
- so let's just quickly talk about what a human message template does
- now we have the settings tab and this one is pretty much the same for all different types of Agents conversational tool plan and execute
- so we've got that and then we have um a system message
- and so we'll do one where it has to reference that to show that but um then it finally just updates the response in the window buffer memory so you can see it this is what we asked what's capital Illinois and then it responded the capital of Illinois Springfield so then I could reference it again and just say like
- so let's try um we'll try to get the calculator to involve so what what is 12 * um [Music] 52 we'll be able to look at the log of what it did so the result of 12 multiped 52 is 624 math can be so much fun can't it
- so that's how that one work works with the log see if there's anything else that we could take a look at in here um I guess you can see right here so right here you know how it says take prompt from previous node automatically um it's looking for an input field called chat input so that's what's right here
- so let me just show that real quick what is um Nvidia so we hit that and we can see it's hitting the brain it's up it updated this and now oh it actually answered just based on the model it didn't even go to Wikipedia um but this is the result we get so it pretty much gives us key areas where Nvidia excels um stuff like that

**CTA / Outro:** "if you're excited about building AI agents within nnn there's so much more to explore feel free to check out other videos on my channel"

**Vocabulary:**
- AI agents
- workflows
- nodes
- tools
- trigger
- webhook
- chatbot
- APIs
- prompt
- system message
- Max iterations
- return immediate steps
- binary images
- automatically pass through binary images
- require specific output format
- output parsers
- autof fixing item list
- structured output parser
- nodes
- log
- buffer memory
- prompt
- Wikipedia
- calculator
- response
- tool
- model
- agent

**Analogies:**
- "think of an AI agent as an employee who has Perfect Memory follows exact instructions never sleeps cost a fraction of hiring a human"
- "so think of this as like you know giving it the personality and the job description down here"
- "it's going to take any binary image images like image files or um you know PDFs from a previous node and it's going to automatically pass through the AI agent node without being changed so this is going to allow you to keep your image files flowing through your workflow alongside other data without the AI agent trying to process it or interpret it as plain text"
- "so the first thing we have is always output data this is going to ensure that um the node outputs data even if it didn't execute a specific action so you want to enable this if you want the workflow to keep flowing regardless of whether the AI agent returned a result or not"
- "think of it like"

**Curiosity Gaps:**
- NOT FOUND
- "I'll get back to this in one sec but first I just want to want to highlight how you know different agents have different options"
- "now we're going to be doing just a live build of an AI agent in nadn we're just going to build out a really simple one give it access to a few tools and just to show some of the aspects of looking at the agent logs um looking at memory seeing the differences in prompting and how that's going to work"
- "so this is sort of the NN builtin one it's super easy to configure because you don't even have to but we've got other options for memory we've got postgress um you can use all this other stuff but going to use window buffer memory here"
- I'll come back to this
- stay till the end
- here's where it gets interesting

**Specificity:**
- "Max iterations"
- "return immediate steps"
- "automatically pass through binary images"
- "require specific output format"
- "output parsers"
- "autof fixing item list"
- "structured output parser"
- "five context window length"
- "we'll leave it as tools and we will configure this stuff in a sec after we give it access to some other stuff"

**Vulnerability:** "I remember being really confused on configuring certain nodes"

**Script Type:** TIGHT

**Energy Notes:**
- [accelerates] when explaining the different types of agents and their uses
- [slows] during detailed explanations of variables and functions

**Audience Language:**
- "you guys"
- "you guys"
- "those of you"
- "OGs"
- "you guys"
- "those of you"
- "OGs"

**Frameworks:**
- "so this is the prompt for the main instruction or the question that the a agent is going to respond to so this is the direct command that that the agent is expected to look through and act on"
- "now we have the settings tab and this one is pretty much the same for all different types of Agents conversational tool plan and execute"
- "so let's just quickly talk about what a human message template does"
- "now we're going to be doing just a live build of an AI agent in nadn we're just going to build out a really simple one give it access to a few tools and just to show some of the aspects of looking at the agent logs um looking at memory seeing the differences in prompting and how that's going to work"

---

## Video 228: Step By Step: Automating Lead Nurturing with No Code in n8n (01/11/24)
**Words:** 5298 | **Chunks:** 2

**Hook:** today I'm going to be walking through step by step how to build this super simple workflow that's going to capture leads information and then automatically email them update in the CRM and then notify your team about this new lead

**Hook Type:** Demonstration

**Credential Drop:** NONE FOUND

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
- first things first
- next it's going to go on to this wait step
- then we have an open AI message and model node
- finally after this step it will go into the slack node
- so as you can see this workflow is currently active so that means anytime a form is actually submitted it will take place
- all right the workflow just finished running
- so here's the response
- all right so this node is configured now we just need to set up that last one which is the slack notification okay
- okay so here's the message we're sending new blank alert
- let me go in here and submit another response and we'll make this one U maybe like a low value lead and we'll see that tag come through and we'll see what the emo looks like

**CTA / Outro:** "if you guys made it all the way to the end thank you really appreciate you guys watching"

**Vocabulary:**
- workflow
- Google Sheets trigger
- wait step
- open AI message and model node
- slack node
- CRM
- lead form responses
- client ID
- client secret
- API key
- automate
- lead nurturing
- no code
- n8n
- Google Sheets
- slack
- node
- workflow

**Analogies:**
- "think of it like"
- "think of it like"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** NONE FOUND

**Script Type:** TIGHT

**Energy Notes:**
- [accelerates] when explaining the workflow steps
- [slows] during detailed explanations of setup processes

**Audience Language:**
- "you guys"
- "you guys"

**Frameworks:**
- "let me hit you with" a very simple use case of sort of capturing some sort of form from a lead magnet it's going to go through and it's going to email them update stuff notify your team but there's also definitely ways you could work off of this like you could have some sort of campaign off of here where you're monitoring This Thread

---

## Video 229: Scrape Google for LinkedIn Profiles in Seconds with n8n (23/10/24)
**Words:** 3611 | **Chunks:** 1

**Hook:** NOT FOUND

**Hook Type:** NOT FOUND

**Credential Drop:** NOT FOUND

**Signature Phrases:** NOT FOUND

**Transitions:** NOT FOUND

**CTA / Outro:** NOT FOUND

**Vocabulary:** NOT FOUND

**Analogies:** NOT FOUND

**Curiosity Gaps:** NOT FOUND

**Specificity:** NOT FOUND

**Vulnerability:** NOT FOUND

**Script Type:** NOT FOUND

**Energy Notes:** NOT FOUND

**Audience Language:** NOT FOUND

**Frameworks:** NOT FOUND

---

## Video 230: n8n Masterclass: Build AI Agents & Automate Workflows (Beginner to Pro) (20/10/24)
**Words:** 20949 | **Chunks:** 6

**Hook:** NOT FOUND

**Hook Type:** NOT FOUND

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
- "you guys"
- "here we go"
- "literally insane"
- "let me hit you with"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"
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
- now it's time to finally hop back into NAD
- all right we are in a Google sheet this is going to be the customer order data that we'll be using for this example so I had chat gbt make up some data for us
- so we know the first step that we always need to do is add some sort of trigger
- now we can configure the rest of this node it's going to be running every minute and that's when it's going to be checking for if a row was added or updated
- So based on this information that it's getting right here
- Now we're back in n8n and we're pretty much done with this workflow
- Okay now we're moving into part three of this master class which is going to be talking about Rag and Vector databases
- next thing we need to do is add a Google Drive node
- so the first step is going to be a chat message because we want to talk to the agent in order for the workflow to start execution so we'll click on chat message
- let's hop back over to Pine Cone let's go to our database
- so now let's just hop into nadn and we can take a look at you know this assistant
- moving on to part five which is going to be talking about apis and HTTP request quests um this kind of stuff can sort of get a little Technical and seem confusing but I'm here to make sure we just sort of break it down as simple as possible so before we really get into the content of this part i wanted to just stress that you know we've already been working with API calls and API tools whether you've known it or not all of the preconfigured nodes in nadn are pretty much just HTTP requests in some way or another so when you're using these nodes naden is doing all that hard work of making the API call for you
- so let's just get into NN real quick and just look at a few examples of an HTTP request node and sort of what it looks like to configure something like that
- now that that concept of just how you access endpoints and how you actually send or receive data makes more sense
- all right we have now made it to part six which is going to be the final part of this master class
- so let's just ask it to do something like can you get my emails this should airor

**CTA / Outro:** "if you guys have made it this far really appreciate you sticking it through all the way"

**Vocabulary:**
- logic nodes
- decision makers
- conditional check
- pause the workflow
- Google Sheets trigger
- client ID and client secret
- API key
- JavaScript variable
- system prompt
- customer success team
- order ID
- customer name
- product quantity
- price
- status
- email subject
- email body
- Json
- Gmail node
- credential
- Vector
- pine cone
- namespace
- embedding
- PDF
- agent
- tools
- workflow
- prompt
- database
- calendar
- email
- slack
- teams
- node
- automate
- workflows
- webhook
- API
- trigger
- node
- error
- telegram

**Analogies:**
- "it's going to be a nice simple example but it's going to feature different types of nodes and we'll be able to see the data move through real time so it'll give us a really good base"
- "so as you can see the resource is text the operation is messaging a model and now we need to choose what model we want to message so I'm going to come in here and grab GPT 40 right there"
- "think of it like"
- "it's basically embedding but with a twist"
- "think of it as the bridge that is going to allow two different softwares to talk to each other like nadn and Google Drive whatever it may be"
- "so we have the API this is like the restaurant itself so this is the service that you're talking to the restaurant is going to provide different services to its customers you know just like an API the restaurant offers a menu of things that you can request different actions or different data then we have the API endpoint the API endpoint is like this specific kitchen station that you're talking to"
- "so in this case you know we wanted spaghetti that's how we know to get it to the right spot but um you know you look you you'd order the specific meal and then um that's just making the request um for data or for a specific service from the API and then finally we have the HTTP request which like we said is pretty much just the mechanism that's being used to deliver the request so in this analogy it's going to be a waiter who's going to take your order bring it to the kitchen staff and then when they bring the dish the waiter is going to bring back that food to bring back that information that you were looking for"
- "so we've got two gets so we'll be asking for information in one way or another and then this last one will show a post where we're actually sending information somewhere"
- "think of it like"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"
- NOT FOUND
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"
- "I remember when I first heard about all these different terms I thought to myself like that sounds so similar how do you really distinguish"
- "so yeah the an NN they know exactly what to do exactly where to go where to send their requests and how to get the information you need or put information somewhere that you need to so now we can move into talking about apis"
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** NOT FOUND

**Script Type:** NOT FOUND

**Energy Notes:** NOT FOUND

**Audience Language:**
- "you guys"
- "those of you"
- "if you've been with me"
- "let me hit you with"
- "literally insane"
- "honestly"
- "crazy"
- "insane"
- "wild"
- "you guys"
- "you guys"
- "those of you"
- "OGs"
- "you guys"
- "those of you"
- "if you've been with me"
- "you guys"

**Frameworks:**
- "first we're going to do here is I'm just going to make this a manual trigger in the future you could have this where every time you upload a document to a certain drive it would do a Google Drive trigger and then it would automatically push that information into pine cone"
- "next thing we need to do is add a Google Drive node because we need to get that information from Google Drive drive into NN so we're going to click on this plus button"
- "the first step is going to be a chat message because we want to talk to the agent in order for the workflow to start execution so we'll click on chat message"
- "so let's just get into NN real quick and just look at a few examples of an HTTP request node and sort of what it looks like to configure something like that"
- "the more realistic use case when you're building stuff like this"
- "so let's say you want to get notified um but then let's say that we want to you know send an email to the team that says hey this this isn't working right now"

---

## Video 231: Step-By-Step: Add 100+ Files to Pinecone for RAG AI Agent with n8n (18/10/24)
**Words:** 3288 | **Chunks:** 1

**Hook:** a few weeks ago I made a video about an RG AI agent where we pushed a PDF into a vector database and then we were able to chat with the agent to get answers from the PDF so after that video a lot of people started asking me well what if we have hundreds of PDFs or hundreds of different documents that we want to push into a vector database and have that database keep growing and we don't want to have to manually you know test workflow every time in order to send it through into pine cone every single time so in this video that's what we're going to be doing

**Hook Type:** Problem-Statement

**Credential Drop:** NONE FOUND

**Signature Phrases:**
- "you guys" the amount of support and feedback I've been getting from you all has been overwhelming and I've been super happy to hear that you guys are learning from my content and enjoying the content
- "here we go" now that you've got all your information that you want in your database into a single folder let's hop into naden
- "let me hit you with" so for the purpose of this video I'm going to be pretending that I own a restaurant and I have all this information that I want to use for an internal sort of agent where my staff can ask questions about our current reviews current menu changes promotions uh policies stuff like that could also be great for training but what we have here is all the information
- "literally insane" so just keep that in mind this is binary data
- "let's not waste any time"
- "honestly" I haven't tested with hundreds but you definitely could do that I've done that in the past where you don't Loop and it's fine
- "crazy" if you did have hundreds and hundreds I don't know if you'd be able to just take all 14 and put them straight into pine cone

**Transitions:**
- so for the purpose of this video I'm going to be pretending that I own a restaurant
- now that we're ready to start building the workflow we have to add the first step which is always going to be a trigger so we're going to do trigger manually here just so we can hit it test workflow and then it will you know search the folder grab the files put them into pine cone for us but in the future once you already have your original database set up and all you need to do is add more information to it you could have this trigger be like a Gmail folder trigger that way every time you add a file to that folder that it's pulling from then it will run through and just put it in the database for you automatically so you don't have to come back here and test it manually but that's um you know in the future
- so we've got our trigger now we want to go and grab a Google Drive node to be able to actually um find the folder that we're searching through

**CTA / Outro:** please hop into the school Community the link will be down in the description it's 100% free it's really nice to get to interact with you guys

**Vocabulary:**
- RG AI agent
- vector database
- pine cone
- Google Drive
- n8n

**Analogies:**

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting" so just keep that in mind this is binary data

**Specificity:**
- [dollars] 
- [percentages] 
- [subscribers] 
- [time_references] a few weeks ago, a lot of people started asking me
- [named_tools] n8n, pine cone

**Vulnerability:** "NONE FOUND"

**Script Type:** LOOSE

**Energy Notes:**
- [accelerates] so just keep that in mind this is binary data so now what we want to do is we want to add a loop and we're doing it this way because you know I have 14 files but if you did have hundreds and hundreds I don't know if you'd be able to just take all 14 and put them straight into pine cone
- [accelerates] so for the purpose of this video I'm going to be pretending that I own a restaurant
- [slows] so we've got our trigger now we want to go and grab a Google Drive node to be able to actually um find the folder that we're searching through so we're going to grab search files and folders I know it's a little confusing because you see like download file you see these folder actions but we're going to be searching files and folders to find the folder

**Audience Language:** "you guys"

**Frameworks:**
- Step-By-Step: Add 100+ Files to Pinecone for RAG AI Agent with n8n

---

## Video 232: I Built an AI Agent that Automated my Inbox with n8n (No Code) (15/10/24)
**Words:** 4871 | **Chunks:** 2

**Hook:** so what you're looking at right here is an inbox management agent I was able to build this thing in about 25 to 30 minutes using absolutely no code so by the end of this video you guys should all understand what's taking place in this workflow and how you can get one of these things up and running within your own email to completely manage your inbox and almost completely remove yourself out of the process of emails

**Hook Type:** Time-Bound

**Credential Drop:** NOT FOUND

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
- "you guys"
- "here we go"
- "let me hit you with"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"

**Transitions:**
- so for example
- one thing I wanted to point out is that this section of the workflow
- and it's also going to telegram us what happened and why it happened so we're going to break down each node each path so that everyone can understand what exactly is taking place here and we'll do a demo for each one too
- back in N end
- now we're going to open up a Gmail node that is to create a draft
- so now we're going to go into this open AI node where we're actually creating the email
- same as all the other ones came in triggered got labeled right away and then we're coming into another open AI node here

**CTA / Outro:** "that's it for today's video so thanks guys"

**Vocabulary:**
- inbox management agent
- classifier
- draft
- telegram notification
- high priority emails
- Nate herkelman
- Gmail
- model 40
- variables
- parameters
- draft
- telegram
- node
- Gmail
- prompt
- model
- trigger
- flow

**Analogies:**
- "it's going to save me a ton of time"
- "think of it like"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** NONE FOUND

**Script Type:** TIGHT

**Energy Notes:**
- [accelerates] when explaining the workflow and actions
- [slows] during detailed explanations of nodes and paths

**Audience Language:**
- "you guys"
- "you guys"

**Frameworks:** NOT FOUND

---

## Video 233: Build a No-Code AI Chatbot (Step-by-Step Tutorial) (14/10/24)
**Words:** 4919 | **Chunks:** 2

**Hook:** today I'm going to be walking through step- by-step how to build an AI chatbot with absolutely no code by the end of this video you'll be able to have this thing up and running on your website for free

**Hook Type:** Time-Bound

**Credential Drop:** NONE FOUND

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
- "you guys"
- "let's not waste any time"
- "literally insane"

**Transitions:**
- so let's get straight into the next step of this video
- now we're actually inside of catling as you can see on the left hand side
- let's go in here into knowledge base because this is what we want to set up first
- now we're in the Builder
- so let's preview the bot and see how information is moving through
- so super easy to put on the website that took no code took me about you know 30 seconds actually after I remembered to publish the app but now let's hop back into chatlink and just be able to make sure we can see this conversation come through okay
- we're back in chatlink

**CTA / Outro:** "if you're interested in maybe some more complicated builds please let me know in the comments what type of stuff you want to see on chatlink and I'll definitely be sure to make a video about it"

**Vocabulary:**
- No-Code
- AI chatbot
- Lead generation
- Deploy
- Conversation
- FAQs
- Knowledge base
- Variables
- AI configuration
- Delay
- No-Code
- AI Chatbot
- publish the app
- conversations
- sources

**Analogies:**
- "think of this as sort of the memory of a chatbot"
- ""

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"
- ""

**Specificity:** NOT FOUND

**Vulnerability:** NONE FOUND

**Script Type:** TIGHT

**Energy Notes:**
- [accelerates] when explaining the benefits of AI chatbots
- [slows] during detailed explanations of the builder interface

**Audience Language:**
- "you guys"
- "those of you"
- "if you've been with me"
- "you guys"

**Frameworks:**
- "one of the really cool things about chatlink is that you can either start from scratch or you can start from one of the templates they have"
- "so let's break it down real quick"
- "now we're going to create a chatbot so one of the really cool things about chatlink is that you can either start from scratch or you can start from one of the templates they have"
- "let's preview the bot and see how information is moving through"
- "so let's get into some of these blocks"
- ""

---

## Video 234: I Built a Personal Assistant AI Agent with No Code in n8n (12/10/24)
**Words:** 5764 | **Chunks:** 2

**Hook:** I'm super excited to share this AI agent build with you guys today I definitely think that it's going to change the way that I do my business especially anything personal Administration related

**Hook Type:** Curiosity-Gap

**Credential Drop:** NOT FOUND

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
- so this is the build right here
- now let's look at what's actually taking place within this agent workflow
- since the demo we just did was forget emails we might as well hop into this one first
- what I think makes the most sense when I'm showing you guys each of these little workflows is actually seeing live data move through
- now let's hop into the execution of that workflow in order to see the data passing through all
- so now we're going to do the send email workflow which is right here
- now let's go into the actual execution of what just took place and look at the data moving through there too
- okay so now we're in the workflow of the tool that gets calendar events and then spits them back out in a nice in a nice short summary
- The Next Step here is taking this information into a calendar node
- now we can see it output sort of some information for us
- but at this point this note is done so we can move on to the last step which is just informing the agent that we did the task once again we do this with an edit Fields set node and this time we added a field called response and we put the response value to done so that the agent knows that we're done
- let's hop into the actual execution of what we just asked telegram to do all right thank goodness for another four node workflow they're super simple and really it's just two nodes because the set and the trigger don't really count but as you can see it's another trigger and it's saying update the AI tool project status to complete and notes to complete so it split that up into two different things which was awesome because it knows that it wants to change the status and the notes not just one or the other
- let's hop into um this database real quick so we can give a look at what's going on and then we will ask it to please um summarize our database

**CTA / Outro:** "I hope all that makes sense and I hope that it was useful for you guys to see actual data moving through each of these steps so that's really about it for this video"

**Vocabulary:**
- personal assistant
- telegram
- node
- workflow
- GPT
- Pine Cone
- embedding
- database
- calendar event
- summary
- node
- workflow
- calendar
- event
- Google Sheets
- database
- project
- status
- notes
- AI

**Analogies:**
- "think of it like"
- "it's basically just all the summaries of all of the projects that the openi node gave us"

**Curiosity Gaps:**
- I'll come back to this
- stay till the end
- here's where it gets interesting
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** "sometimes you just have to outline that"

**Script Type:** LOOSE

**Energy Notes:**
- [pace_accelerates] so this is the build right here as you can tell the way that we're interacting with our agent is through telegram so I can pull that up on my phone or on my desktop and all I have to do is ask it to do something for me it's going to run through through this logic and then it's going to Output either a result to me or it's going to tell me that hey I went in the back end and I did that for you you know updated the database or set a calendar event whatever it may be so I'm going to walk through exactly what's going on in each step and we'll jump into each of these sub tools
- [pace_slows] so this first node is an open AI node and as you can see the first thing that we wanted to do was give it a prompt so I said your job is to identify what date the user is asking for based on the Json query and what the current date is so I gave it the current date of now this is a JavaScript script code it just says you know dollar sign now and that Returns the date time of what is right now current so that's all that's happening right there and then I gave it two examples the first one is if the query asks for today you would return today's date and if the query asks for yesterday you would return the day before yesterday and sometimes you just have to outline that um it might seem self-explanatory but open AI doesn't always know that you know yesterday was the day before or two days ago was going to be today's date minus two so giving it examples in ensures that it's as consistent as possible

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"
- "you guys"

**Frameworks:** NOT FOUND

---

## Video 235: How to Build a Client Onboarding AI Agent with n8n (Step-by-Step Tutorial, No Code) (09/10/24)
**Words:** 4719 | **Chunks:** 2

**Hook:** in this step-by-step tutorial I'm going to be walking through how to build this workflow where we're going to be utilizing two different agents in order to get rid of some of the tedious and time-consuming stuff that comes along with onboarding a new client by the end of this video you'll have this workflow up and running and you can do so with using absolutely zero code

**Hook Type:** Problem-Statement

**Credential Drop:** NOT FOUND

**Signature Phrases:**
- "let's not waste any time"
- "literally insane"
- "honestly"
- "you guys"
- "here we go"
- "let me hit you with"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"

**Transitions:**
- "so with that being said the first step that we're going to do here is going to be an nadn form trigger"
- "okay so we've got the fields filled out"
- "and then at the end I just like to click on options add option append NAD n attribution and then just turn that off it just makes the form look a little cleaner"
- so next we're going to add our first AI agent
- the next thing that we want to do here is we want to actually add the Gmail node
- let's click on the plus button and we're going to add another AI agent
- now let's move on to the next step

**CTA / Outro:** "if you're interested in seeing how you could expand off of a client in boarding form trigger like this please let me know in the comments"

**Vocabulary:**
- tutorial
- step-by-step
- client
- onboarding
- agents
- form trigger
- email
- spreadsheet
- automatically
- required fields
- pin
- node
- workflow
- form submission
- client onboarding
- AI agent

**Analogies:**
- "think of it like"

**Curiosity Gaps:**
- "and then the second one is that it's going to take their client profile give a nice summary and put it into a spreadsheet for us automatically so we can see all of our new clients in one Consolidated place"
- "so with that being said the first step that we're going to do here is going to be an nadn form trigger"
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** NONE FOUND

**Script Type:** TIGHT

**Energy Notes:**
- [pace_accelerates] "and then the second one is that it's going to take their client profile give a nice summary and put it into a spreadsheet for us automatically so we can see all of our new clients in one Consolidated place"
- [pace_accelerates] "so with that being said the first step that we're going to do here is going to be an nadn form trigger"
- [pace_slows] "and then at the end I just like to click on options add option append NAD n attribution and then just turn that off it just makes the form look a little cleaner"

**Audience Language:**
- "you guys"
- "those of you"
- "if you've been with me"
- "you guys"

**Frameworks:**
- "in this step-by-step tutorial I'm going to be walking through how to build this workflow where we're going to be utilizing two different agents in order to get rid of some of the tedious and time-consuming stuff that comes along with onboarding a new client"
- "so within this s in form trigger node we can see we've got the URL that's what you're going to be able to send to the client in order for them to fill it out"

---

## Video 236: How to Build a Google Scraping AI Agent with n8n (Step By Step Tutorial) (06/10/24)
**Words:** 4123 | **Chunks:** 1

**Hook:** so today I'm going to be walking through step by step how to build this Google scraping AI agent in n8n (Step By Step Tutorial)

**Hook Type:** Demonstration

**Credential Drop:** NOT FOUND

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

**Transitions:**
- so let's hop into a quick demo real quick so we can see how the agent works before we actually see how to build this thing
- now that we've seen a demo of how we chat with the agent and how it actually works let's move into what we need in order to build this thing
- okay so here's our information the next step is to connect an open AI node so we're going to go grab an open AI and message a model
- now the last thing we need to do is we need to add a set node which we're going to name this field response with the value of done

**CTA / Outro:** "please leave a like if you've enjoyed and definitely let me know in the comments what else you guys want to see so I can continue to add to my list of videos that I want to make and stuff to learn about so that I can sort of help all you guys out"

**Vocabulary:**
- walk through
- step by step
- workflow
- agent
- tool

**Analogies:** "imagine"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:**
- [named_tools] n8n

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] "so today I'm going to be walking through step by step how to build this Google scraping AI agent in n8n"
- [accelerate] "so here's the agent it's super simple we've only got these three tools here"
- [slow] "so let's hop into a quick demo real quick so we can see how the agent works before we actually see how to build this thing"
- [slow] "now that we've seen a demo of how we chat with the agent and how it actually works let's move into what we need in order to build this thing"

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"
- "if you've been with me"

**Frameworks:**
- "so the first one is going to be the tool that scrapes Google for the URLs and then the second one is the actual agent that we can interact with so that's all for the prep stage let's hop back into n8n and let's start a new workflow and start building this thing"
- "okay so here's our information the next step is to connect an open AI node so we're going to go grab an open AI and message a model"

---

## Video 237: *LIVE BUILD* Inbox Management AI Agent with n8n (NO CODE, Step-by-Step Tutorial) (02/10/24)
**Words:** 3098 | **Chunks:** 1

**Hook:** all right today we're going to be building a inbox management agent by the end of this video you'll have a workflow up and running that is going to be able to categorize and label your emails as they come in based on how you tell the agent to do so

**Hook Type:** Problem-Statement

**Credential Drop:** NOT FOUND

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

**Transitions:**
- so the first thing we need to do as always is add a first step which is something that triggers the workflow to actually run
- the next node we're going to add is the actual agent it's going to be a text classifier so when we're in here the first thing that we need to set up is what text is this node classifying
- branching off the high priority let's click on the plus and we're going to grab a Gmail node again this one is going to be right here at the top add label to message

**CTA / Outro:** "if you enjoyed definitely leave a like and let me know what else you want to see but other than that thanks so much guys"

**Vocabulary:**
- inbox management
- Gmail trigger
- credential
- API key
- text classifier
- labels
- node
- workflow

**Analogies:** "think of it like"

**Curiosity Gaps:**
- I'll come back to this
- stay till the end
- here's where it gets interesting

**Specificity:**
- [time_references] every minute
- [time_references] 25 seconds
- [named_tools] n8n
- [named_tools] Google Cloud
- [named_tools] Gmail API
- [named_tools] OAuth consent screen

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [accelerates] "so the first thing we need to do as always is add a first step which is something that triggers the workflow to actually run"
- [accelerates] "the next node we're going to add is the actual agent it's going to be a text classifier so when we're in here the first thing that we need to set up is what text is this node classifying"
- [slows] "so let's real quick send an email that would be a high priority message"
- [slows] "let me just move this over and as you can see we've got a high priority email"

**Audience Language:**
- "you guys"
- "those of you"
- "if you've been with me"

**Frameworks:**
- "so the first thing we need to do as always is add a first step which is something that triggers the workflow to actually run"
- "the next node we're going to add is the actual agent it's going to be a text classifier so when we're in here the first thing that we need to set up is what text is this node classifying"
- "branching off the high priority let's click on the plus and we're going to grab a Gmail node again this one is going to be right here at the top add label to message"

---

## Video 238: *LIVE BUILD* Personalized Outreach AI Agent in n8n (No Code) (26/09/24)
**Words:** 4627 | **Chunks:** 2

**Hook:** okay so today I'm going to be doing a live build of an AI agent this agent is going to qualify leads and going to generate a personal message for each lead

**Hook Type:** Demonstration

**Credential Drop:** NOT FOUND

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
- "you guys"
- "let me hit you with"
- "literally insane"

**Transitions:**
- so the agent will call this tool in order to start the process of moving it through this logic
- now let's move on to the next step
- so we're done with this one now we're going to add another message
- next step here is we need to add another sheets node so that this information actually goes back into Google Sheets
- so let's say we got an error with the personal message tool
- that's going to do it for this one

**CTA / Outro:** please let me know what else you guys want to see and if you sort of like these live builds or step by steps let me know too and yeah that's all so thanks guys

**Vocabulary:**
- live build
- lead database
- Google Sheets
- Google form
- qualification status
- personal message
- open AI
- API key
- merge node
- data transformation
- personalized outreach
- AI agent
- n8n
- executions
- workflows

**Analogies:**
- "it's pretty much we're getting we're getting the information from the database we're doing something to get some sort of answer to put back onto the row and then we're actually putting it back onto the row"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [accelerates] discussing the workflow setup and node connections
- [slows] explaining the steps in detail, such as setting up credentials for nodes

**Audience Language:**
- "you guys"
- "those of you"
- "if you've been with me"
- "you guys"

**Frameworks:** NOT FOUND

---

## Video 239: Build your first NO CODE AI Agent in n8n (for beginners) (25/09/24)
**Words:** 3736 | **Chunks:** 1

**Hook:** today I'm going to be walking through step by step how to build this AI agent in Ann no prior coding experience is needed you'll be able to get this agent up and running within 15 minutes so by the end of it you'll have a great idea of how to build Tools in NN and how to have agents call different Tools in order to be as effective as possible

**Hook Type:** Demonstration

**Credential Drop:** NOT FOUND

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

**Transitions:**
- so the workflows we're going to be building today just two of them
- now let's go and get into actually building this thing
- okay so back to nadn okay so we're going to add a new workflow
- let's actually not prompt this one because I want to show you guys what it does when we just leave it as helpful assistant

**CTA / Outro:** "if you enjoy this type of cont content please let me know"

**Vocabulary:**
- walk through
- step by step
- prior coding experience
- up and running
- great idea
- effective
- API key
- workflow

**Analogies:** "think of it like"

**Curiosity Gaps:**
- I'll come back to this
- stay till the end
- here's where it gets interesting

**Specificity:**
- [time_references] 15 minutes
- [named_tools] open weather map
- [named_tools] open AI API

**Vulnerability:** "I'm going to disable this one after the video because I'm exposed now"

**Script Type:** LOOSE

**Energy Notes:**
- [pace_accelerates] so let's ask it what is the capital of Florida we get the capital of the US state of Florida is Tallahassee if you need any information about Tah has or anything else feel free to ask
- [pace_slows] so the workflows we're going to be building today just two of them
- [pace_slows] now let's go and get into actually building this thing so the resources needed here are going to be nadn the weather API and open AI API

**Audience Language:** "you guys"

**Frameworks:**
- the first one is the tool the git current weather tool and then we'll be giving the agent access to that tool and so the second workflow is the AI agent

---

## Video 240: How to Create an RAG Chatbot AI Agent with n8n (No Code, Step-by-Step Tutorial) (23/09/24)
**Words:** 3315 | **Chunks:** 1

**Hook:** today I'm going to be walking through step by step how to build this super simple question and answer AI agent like it says right there no code basically this agent is going to take information you give it so information about a company large database whatever it might be and then you're going to be able to chat with it to get the answers you need quicker than if you were to manually have to search through a document or multiple documents

**Hook Type:** Demonstration

**Credential Drop:** NONE FOUND

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
- so let's just get into the rest of this video
- let's see how we're going to build this thing
- the first workflow I said that we were going to be doing is um pushing the DAT into pine cone so we're just going to call this one push data
- now we're going to add in the actual entity of the agent

**CTA / Outro:** "if you enjoyed you know please let me know what what else you want to see"

**Vocabulary:**
- super simple
- quickly
- concise
- vector database
- large language model
- pine cone
- Google Drive
- Open AI API

**Analogies:** "it's basically a way for agents to search through large amount of data much quicker than with a traditional relational database"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:**
- [time_references] 23/09/24
- [named_tools] Pine Cone
- [named_tools] Google Drive
- [named_tools] Open AI API

**Vulnerability:** "I'm not going to do that cuz I already have one like I said"

**Script Type:** LOOSE

**Energy Notes:**
- [accelerates] discussing the workflow steps and tools
- [slows] explaining credentials setup for Google Drive

**Audience Language:** "you guys"

**Frameworks:**

---

