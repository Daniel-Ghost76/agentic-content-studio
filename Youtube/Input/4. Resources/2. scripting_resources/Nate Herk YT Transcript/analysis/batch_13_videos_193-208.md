# Batch 13: Videos 193-208

## Video 193: I Built an AI Voice Travel Agent with ElevenLabs and n8n (Free Template) (16/02/25)
**Words:** 7678 | **Chunks:** 3

**Hook:** hey there I'm Jessica how can I help you today

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
- so let's go take a look okay
- all right so as you can see in the demo this is what the workflow looks like
- we'll dive into the actual 11 Labs configuration of the agent we'll dive into all of these nodes here in NN and see what's going on
- so this is the custom one that we set up
- now in these tools you have the options to set up your
- so now we're going to set up the different properties
- cool so from there we're passing it into a basic llm chain
- so the first one we're doing is the activities request
- so this is where you can really start to customize the information that you want your agent to see
- because finally after the nearby places I think below the images I was able to drag in right here the list of amenities so when I drag in the list of amenities it pops up with all the stuff like air conditioning crib ironing board board kitchen smoke free all that kind of stuff um so that helps too
- so then of course as you can imagine for um Resorts two and three I did the exact same thing I just close out of property zero open up property one and then drag in the same information once again okay
- then finally at the bottom activities it's a lot easier we're going to open up the activities Tav request we can see our query was Riverboat tour in Chicago and then we have three results I'm only going to drag two in for this example but I dragged in the title of the activity the URL for the activity and then the description and then I just did the exact same thing for activity number two which are kind of the same things but just two different sources to look at
- but as you can see that is what the agent is now getting and using that information it creates an email based on these guidelines that we gave it in the system prompt so that is how it was able to you know insert these horizontal lines it made an intro section that was exciting it talks about our flights ites does the images 20% rather than making them huge 100% um so all this kind of stuff right

**CTA / Outro:** as always really appreciate you guys making it to the end of this one if you learned something new or you just enjoyed it please give it a like definitely helps me out a ton but really appreciate you guys making it to the end and thank you see you guys in the next one

**Vocabulary:**
- travel agent
- web hook
- voice agent
- n8n
- email agent
- token usage
- static knowledge base
- end call system tool
- web post URL
- llm Prompt
- Dynamic variables
- airport codes
- structured output parser
- Ser API
- HTTP requests
- dragged in
- rate per night
- total rate
- nearby places
- amenities
- activities
- subject
- body

**Analogies:**
- "it's going to look like this and we're going to go over what you need to configure to get this thing up and running"
- "it's going to be a post because what we're doing is we're trying to send over data to nadn to run it through these different apis and then create an email so that's why it's going to be a post"
- "so this is the one I click to copy this and then I pretty much paste that right in there"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"
- "I'll show you guys that anyways you could specify that here as well"
- "now what's next is we need to format some of this stuff because first of all when we're putting in our requests to you know the resort or the um flights we don't want to use these city names what we want to do is use airport codes so we have to get the airport codes and then we also have to turn these dates from strings into date format"
- "so this is where we're using the brain of the AI and the structured output parser which you can see right here"
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:**
- "we don't really need to do so because we're using basically search functionality to get all the information back"
- "so first thing to note is that the agent will likely by default have this end call system tool which just gives the ability to the agent to end the call if it knows it's over"
- "so you'll click on ad tool Custom Tool and then this is where we configure everything so this is the screen you'll see"
- "we're trying to send over data to nadn to run it through these different apis and then create an email so that's why it's going to be a post"
- "so if I go back into my naden click into this web hook you can see the post request endpoint right here"
- "so we have the name andn then we gave it this description which is this tool generates a travel plan once the details are collected"
- "we have the URL right here which is just the web post URL from naden"
- "so first of all we gave it the name andn then we gave it this description which is this tool generates a travel plan"
- "so now what's next is we need to format some of this stuff because first of all when we're putting in our requests to you know the resort or the um flights we don't want to use these city names what we want to do is use airport codes so we have to get the airport codes and then we also have to turn these dates from strings into date format"
- "so this is where we're using the brain of the AI and the structured output parser which you can see right here"

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [accelerates] "so let's go take a look okay"
- [accelerates] "all right so as you can see in the demo this is what the workflow looks like"
- [slows] "it's going to look like this and we're going to go over what you need to configure to get this thing up and running"

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"
- "if you've been with me"
- "you guys"
- "so now what's next is we need to format some of this stuff because first of all when we're putting in our requests to you know the resort or the um flights we don't want to use these city names what we want to do is use airport codes so we have to get the airport codes and then we also have to turn these dates from strings into date format"
- "so this is where we're using the brain of the AI and the structured output parser which you can see right here"
- "you guys"
- "those of you"
- "OGs"
- "if you've been with me"

**Frameworks:**
- "we're going to go over it at a pretty high level if you're looking for a more Hands-On approach and you want to see the step-by-step build and definitely check out the paid Community"
- "first thing to note is that the agent will likely by default have this end call system tool which just gives the ability to the agent to end the call if it knows it's over but then this is the custom one that we set up so you'll click on ad tool Custom Tool and then this is where we configure everything so this is the screen you'll see"
- "so now in these tools you have the options to set up your you know header parameters path parameters query parameters we don't need to do that all you want to do is enable body parameters and this is actually going to be the things that we the attributes that we set up to have the 11 Labs Gemini 2.0 flash model look at the trans script when it's conversating with us pull out these details and send them to anen so first of all we describe how this is going to work we say collect all of these details from the caller then send the request"
- "so now we're going to set up the different properties we want to pass over the first one is return date we're saying that this is a string data type we're going to be pulling this from The llm Prompt rather than using Dynamic variables and then we describe it as the day the caller wants to return"
- "so now what's next is we need to format some of this stuff because first of all when we're putting in our requests to you know the resort or the um flights we don't want to use these city names what we want to do is use airport codes so we have to get the airport codes and then we also have to turn these dates from strings into date format"
- "so this is where we're using the brain of the AI and the structured output parser which you can see right here"

---

## Video 194: This Trick Helps me Build Agents 3x Faster (as a beginner) (12/02/25)
**Words:** 3610 | **Chunks:** 1

**Hook:** today I'm going to be talking about the technique that I use to build the ultimate assistant workflow in under an hour now that won't include final testing and refining and airor handling but the point of this video is that if you don't know this method or if you kind of know about it but don't really understand it and you start to use it after this video it's going to help you build agents three times faster

**Hook Type:** Time-Bound

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
- so let's get back to the video
- now let's do a different tool
- if you come into here everything else is going to be pretty much the same
- let me hit you with this one

**CTA / Outro:** "as always really appreciate you guys making it to the end of this one if you appreciated it if you learned something new please give it a like"

**Vocabulary:**
- assistant workflow
- ultimate assistant
- AI agent
- tools
- node configuration
- send email tool
- Outlook Integrations
- email body
- prompting
- current date and time

**Analogies:** "think of it like"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:**
- [time references] under an hour
- [named tools] Outlook
- [named tools] Tavali

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [pace accelerates] so what is the method that we're going to be talking about today
- [slows down] let's hop over to a quick visualization that I made and then we're going to look at some examples in nadn and I'll show you guys how quickly we can spin something up okay so here we are in excal draw and I have a visualization that I made which is going to explain this process hopefully really simply break it all down

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"
- "if you've been with me"

**Frameworks:**
- "today I'm going to be talking about the technique that I use to build the ultimate assistant workflow in under an hour now that won't include final testing and refining and airor handling but the point of this video is that if you don't know this method or if you kind of know about it but don't really understand it and you start to use it after this video it's going to help you build agents three times faster"
- "so what is the method that we're going to be talking about today well when you're creating an AI agent and you want to give it access to tools you'll click on this plus and on the right you'll have a bunch of tools right here and what we're looking at are these Integrations where we have nodes as tools so in this case we would have clicked on Gmail tool and then we have these pop up and then within there we have to configure certain things so in this send email tool for example we have to configure who's the email going to what's the subject of the email and then what is the message of the email in order for the agent to actually be able to send it"
- "so let's hop over to a quick visualization that I made and then we're going to look at some examples in nadn and I'll show you guys how quickly we can spin something up okay so here we are in excal draw and I have a visualization that I made which is going to explain this process hopefully really simply break it all down"
- "so let's do a different tool so let's look at using Outlook again but this time we're going to be um creating a calendar event so I'm going to do event I'm going to do create and now you can see we have three Fields once again that we need to set up the functions so the AI can figure out how to populate these parameters"
- "so let's say we want to do something in slack we would basically just send the message to um you know we could choose our Channel but when it actually comes to the message all I have to do is come in here um choose the dollar sign from AI function and then just to find the key so all of these nodes as tools are going to have different parameters to send across and all you have to do is basically tell the AI when you're you know filling out this section this is what you're looking for"
- "so now that we understand how the from a function works and how quickly and easy it is to set up some of these different tools now it's just a matter of plugging them in testing them and adding more so we started off with something like a send email we test it out once we know it works we can start to add more and more and as you can see I was able to add all of these and then you obviously want to give it sort of a system prompt where you're in here and you're telling it what each tool does as you can see this prompt still isn't too long or complex at all but then from there it's just about manipulating the logic so that you can get what you need within each parameter"

---

## Video 195: 4 Agentic Frameworks for More Efficient Workflows in n8n (10/02/25)
**Words:** 4319 | **Chunks:** 2

**Hook:** so in my ultimate assistant video we utilize an agentic framework called parent agent so as you can see we have a parent agent right here which is the ultimate assistant that's able to send tasks to its four child agents down here which are different workflows that we built out within naden

**Hook Type:** Problem-Statement

**Credential Drop:** NONE FOUND

**Signature Phrases:**
- "you'll come in here click on YouTube resources"
- "let me hit you with"
- "what's really cool"
- "here we go"
- "literally insane"

**Transitions:**
- so today I'm going to be going over four different agentic Frameworks that you can use in your NN workflows
- back to the video here the first one we're going to be talking about is prompt chaining
- finally it's going to be more scalable and reusable as we're able to plug in different agents wherever we need them okay so what we have to do here is we're just going to enter in a keyword a topic for this um blog

**CTA / Outro:** NOT FOUND

**Vocabulary:**
- ultimate assistant
- parent agent
- child agents
- workflow
- prompt chaining
- routing
- parallelization
- evaluator Optimizer

**Analogies:**
- "think of it like passing the output into the input and then taking that output and passing it into the next input"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] "so in my ultimate assistant video we utilize an agentic framework called parent agent"
- [accelerate] "so today I'm going to be going over four different agentic Frameworks that you can use in your NN workflows"
- [slow] "so the ultimate assistant could get a query from the human and decide that it needs to send that query to the email agent which looks like this"
- [slow] "finally we've got easier debugging and optimization because it's linear we can see where things are going wrong"

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"
- "if you've been with me"

**Frameworks:**
- "so the first one we're going to be talking about is prompt chaining"
- "now we're going to talk about the routing framework"
- "third one is parallelization and the fourth one is evaluator Optimizer so we're going to break down how they all work what they're good at"

---

## Video 196: I Built a Human In The Loop Sales Team That Waits for Feedback and Approval in n8n (05/02/25)
**Words:** 4752 | **Chunks:** 2

**Hook:** today I'm going to be breaking down this awesome team of sales agents that uses humanin thee Loop functionality for feedback and approval so every time a lead form is submitted and captured an air table it's going to send that to this sales agent that's going to write an email and then send it off to us the human not only just for approval but also for feedback if the email gets approved it's going to be sent off to that lead but if it's not it's going to get sent to the revision agent so the revision agent is then going to take the email that the sales agent made it's going to take the feedback from the human and it's going to revise that email and create a new one then as you can see it Loops right back to the human for another round of feedback and approval

**Hook Type:** Demonstration

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
- "what's really cool"
- "let me hit you with"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"

**Transitions:**
- so let's show off a quick demo
- so on the left screen we've got my email as you can see I've been doing a lot of testing and on the right we have the sales agent team so let's hit test workflow
- now what we're going to do is click on respond and it's going to open up this tab where we can actually give feedback
- so now that email got sent off so let's go check on that real quick
- let's break down what's going on within the revision agent
- now let's say it revises it again it comes through and then
- what I want to do now is Show an example where we make like three or four revisions so you can see that it's going to come through every single time

**CTA / Outro:** "if you guys enjoy this one or learn something new please give it a like it really really helps me out and I really appreciate you guys making it to the end of the video"

**Vocabulary:**
- humanin thee Loop
- air table
- sales agent
- revision agent
- Cloud 3.5 sonnet
- human in the loop
- feedback
- approval
- revision agent
- structured output parser
- set email node
- get feedback note
- sales agent

**Analogies:**
- "think of it like"
- "imagine" it's basically a process but with human oversight and input

**Curiosity Gaps:**
- "I'll come back to this"
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** NONE FOUND

**Script Type:** TIGHT

**Energy Notes:**
- [accelerates] so let's show off a quick demo then I'm going to show you guys how you can download this workflow for free and then we'll get in there and break down every single node that you see right here
- [slows] so now what we're going to do is click on respond and it's going to open up this tab where we can actually give feedback so what I'm saying in the feedback is make it more concise because this email is pretty wordy and then I said also don't mention 23% in reduction time right up here and propose that we meet on Thursday so I'm going to hit submit

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"
- "you guys"
- "those of you"
- "OGs"
- "if you've been with me"

**Frameworks:**
- "let's break down what's going on within the revision agent"

---

## Video 197: I Built the Ultimate Team of AI Agents in n8n With No Code (Free Template) (03/02/25)
**Words:** 5918 | **Chunks:** 2

**Hook:** hey guys so what we're going to be looking at today is the ultimate personal assistant and I'm super excited to share this build with you guys as you can see the ultimate assistant has access to these four agents that we built out within nadn

**Hook Type:** Demonstration

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
- "what's really cool"
- "let me hit you with"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"

**Transitions:**
- so right now telegram just sent over that audio file it's getting transcribed now
- here we go in our caler invite you can see that Nate herkelman got added as a guest
- let's quickly refresh our Gmail
- here we go the blog about deep seek has been created and included in a draft email for Nate herkelman
- there we go hitting the calendar agent right now it's getting availability as you can see we only have three meetings today so this is what we should get pulled back um as our sort of unavailable slots
- so this is me signing off
- that's going to be it for this one
- thanks guys so much for watching if you enjoy this one if you liked it then please drop me a like definitely helps me out a lot and let me know in the comments what else you want to see but as always appreciate you guys making it to the end of this one i'll see you guys in the next video thanks

**CTA / Outro:** "thanks guys so much for watching if you enjoy this one if you liked it then please drop me a like definitely helps me out a lot and let me know in the comments what else you want to see but as always appreciate you guys making it to the end of this one i'll see you guys in the next video thanks"

**Vocabulary:**
- ultimate assistant
- agents
- n8n
- telegram
- Nate Herman
- GPT 40
- Claude 3.5 Sonet
- web search functionality
- ultimate team
- AI agents
- n8n
- free template
- from AI function
- prompt
- node
- workflow
- email agent
- personal assistant

**Analogies:**
- "it's going to be aware of what we're talking about when we say can you push that back an hour as you can see it just hit the contact agent now it's hitting calendar and email agent so we're going to watch right here as the team sync gets bumped back an hour"
- "so in this case if you're looking to send emails draft emails or create calendar events with attendees you need to get contact information first and then you use the email agent to send the email and you'll pass the tool a query like send Nate herman an email to ask what time he wants to leave"
- "think of it like"

**Curiosity Gaps:**
- "I'm going to show you guys how you can download this workflow for completely free and then plug it into your nadn and get started"
- "here we have our caler invite you can see that Nate herkelman got added as a guest"
- "let's take a look at the draft real quick"
- I'll come back to this
- stay till the end
- here's where it gets interesting

**Specificity:** NOT FOUND

**Vulnerability:** NONE FOUND

**Script Type:** TIGHT

**Energy Notes:**
- [accelerates] so right now telegram just sent over that audio file it's getting transcribed now
- [accelerates] here we go in our caler invite you can see that Nate herkelman got added as a guest
- [slows] so the ultimate assistant framework is that as you can see this prompt is not very long or not very complex and similarly with all the other agents the prompts are not very long and not very complex so this is really cool because every agent sort of specializes in something rather than loading up one agent with a ton of tools and a huge prompt

**Audience Language:**
- "you guys"
- "those of you"
- "if you've been with me"
- "you guys"
- "those of you"
- "OGs"
- "if you've been with me"

**Frameworks:** NOT FOUND

---

## Video 198: OpenAI Fires Back at DeepSeek With a New Reasoning Model: o3-mini (n8n AI Agent) (01/02/25)
**Words:** 2936 | **Chunks:** 1

**Hook:** so let's go ahead and throw a query at this travel agent and we will see what we get we're asking for it to plan a 5-day trip to Paris with a budget of $2,000 so let's see it's hitting the openai reasoning model right now

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
- so let's go ahead and throw a query at this travel agent and we will see what we get
- now it finished up we'll see what it said back to us
- there we go so we just saw it hit the send itenerary Gmail tool
- as you can see we just got this email back the subject is your 5-day Paris trip
- so that's great it keeps that into account when it's going through and reasoning how to make this itinerary
- what's really cool about 03 is that it's their first small reasoning model that supports highly requested developer features including function calling structured outputs and developer messages making it production ready right out of the gate
- so we played around with deep see we've seen that it's been really really cool but when you try to hook up tools to an agent it's not really supported for that so it'll be really cool to see how o03 mini performs when we give it access to these four different tools and it also has that aspect of reasoning through and creating hopefully a really really nicely structured itinerary based on all the information it's going to get from these databases and what the we ask for up front
- so if you're watching this video later it will probably be here but for now we have a really easy solution which is um we can just connect to open router which thanks to the update that also happened yesterday or the day before um we have the native open a open router chat model now so this is really cool all you have to do is go to open router
- so let's take a quick look at the prompt and then we'll send off another example and see what type of itenerary we get back
- so that's what the database looks like that's where it's getting its information and then the last thing it needs to do is actually send out the email so right now I just put my email it's going to be fixed so every time I activate this agent it's going to send an email to this address rather than being able to dynamically put that in if you want it to do dynamically you could do that super easily by making this an expression and then you utilize the from AI function that we're using in the the subject and the message parameters and just put in from Ai and then the key would be like an email address or recipient or something like that anyways obviously we're sending a message Mage and we wanted to do HTML this time rather than text because we could just get it formatted a little better a little more human readable for us and then finally we just turned off the append naden attribution so that at the bottom of the email it doesn't say that this was generated by naden
- so now we've got that out of the way let's send off one more query to end this one off

**CTA / Outro:** as always really appreciate you making it to the end hope this one was helpful if it was please give it a like definitely helps me out a lot and I will see you guys in the next one

**Vocabulary:**
- travel agent
- itinerary
- budget
- Pine Cone
- open router
- HTML
- Naden
- prompt architect

**Analogies:**
- "so let's go ahead and throw a query at this travel agent and we will see what we get"

**Curiosity Gaps:**
- "I'll come back to this"
- "here's where it gets interesting"
- "what's really cool about 03 is that it's their first small reasoning model that supports highly requested developer features including function calling structured outputs and developer messages making it production ready right out of the gate"

**Specificity:**
- [dollars] $2,000
- [time] yesterday or the day before
- [tools] open router, Pine Cone databases

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- The pace accelerates when discussing the new model's capabilities and its potential impact.
- Slows down during detailed explanations of the workflow setup.

**Audience Language:** "you guys"

**Frameworks:**

---

## Video 199: How to Locally Host DeepSeek R1 for FREE in Under 10 Minutes in n8n (31/01/25)
**Words:** 2353 | **Chunks:** 1

**Hook:** today I'm going to show you guys the quickest and easiest way to get deep seek set up locally so you can use it within NN

**Hook Type:** Problem-Statement

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
- now the fun stuff
- hey guys just wanted to say real quick
- let's get back to the video okay

**CTA / Outro:** if this kind of stuff interests you please check the communities out with the links in the description

**Vocabulary:**
- self-hosted
- API calls
- data security and privacy
- N8n
- DeepSeek R1
- Llama

**Analogies:**

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:**
- [dollars] 
- [percentages] 
- [subscribers] 
- [time_references] 31/01/25
- [named_tools] N8n, Docker, GitHub, AMA

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [accelerates] discussing the privacy policy and API usage
- [slows] explaining the setup process in detail

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"
- "if you've been with me"

**Frameworks:**

---

## Video 200: Best Model for RAG? GPT-4o vs Claude 3.5 vs Gemini Flash 2.0 (n8n Experiment Results) (30/01/25)
**Words:** 4400 | **Chunks:** 2

**Hook:** wow flash was 6.7 seconds GPT was 11 seconds and then open AI or anthropic CLA was almost 21 seconds so that's that's kind of a big jump here

**Hook Type:** Result-First

**Credential Drop:** NONE FOUND

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
- "I'll see you guys in the next one"

**Transitions:**
- so let's hop in NN
- so the first section here is information recall
- okay so we got the response back
- let's quickly look at the way that Gemini did it and as you can see
- for round two we got 798 it's a pretty tight race
- okay so that one just finished up we'll click at executions

**CTA / Outro:** definitely found a like if you found this one helpful or interesting or funny in some way I always appreciate you guys making it to the end of these videos and I'll see you guys in the next one

**Vocabulary:**
- retrieval augmented generation
- vector database
- prompt
- tool calling
- earnings report
- financial and earnings information
- open AI model
- consistent
- different models
- prompt

**Analogies:**
- "it's basically just the process of your agents going out to get information that it doesn't already have in its sort of training data or it's prompt"
- "the r is retrieval it's going out to retrieve the information the a is augmented it pretty much takes that information that gets back from the vector database or whatever database you're sort of having it access it augments that data and information with other stuff that came through in the query and the prompt and then finally it's handing that off to the large language model to create to generate the response that makes sense to the human based on the context of its role and also the query that originally came in"
- "the idea of this EXP experiment is to keep everything as consistent as possible we're going to limit the variability as much as we can by doing the following things"
- "it's like a cool way to keep things consistent and leave it less up to my own inter interpretation"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"
- "so we're going to be answering this question by putting these three popular models to the test"
- "let me hit you with"
- "it's basically what it looks like"

**Specificity:** NOT FOUND

**Vulnerability:** "I'm not like a scientist or an experiment expert but I just thought that this would be a cool way to keep things consistent and leave it less up to my own inter interpretation"

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] wow flash was 6.7 seconds GPT was 11 seconds and then open AI or anthropic CLA was almost 21 seconds so that's that's kind of a big jump here
- [slow] so the r is retrieval it's going out to retrieve the information the a is augmented it pretty much takes that information that gets back from the vector database or whatever database you're sort of having it access it augments that data and information with other stuff that came through in the query and the prompt and then finally it's handing that off to the large language model to create to generate the response that makes sense to the human based on the context of its role and also the query that originally came in

**Audience Language:**
- "you guys"
- "those of you"
- "if you've been with me"
- "you guys"
- "I'll see you guys in the next one"

**Frameworks:**
- "the idea of this EXP experiment is to keep everything as consistent as possible we're going to limit the variability as much as we can by doing the following things"
- "we'll hop into nadn and you'll see the three different agents we have and we'll actually run through this process it'll make a lot more sense"

---

## Video 201: How to Actually Build Agents with DeepSeek R1 in n8n (Without OpenRouter) (24/01/25)
**Words:** 2807 | **Chunks:** 1

**Hook:** so we're going to send off this three-part message to our deep seek planning agent it's going to be taking that input right now it's going to be constructing a step-by-step plan of instructions to hand off to the tools agent

**Hook Type:** Problem-Statement

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
- So lately there's been a ton of hype around deep seeks new reasoning model
- the first issue like I said you guys may be experiencing is calling it through open router where we are setting up a credential with the base URL of open router.
- if we want to connect to deep seek like this what you're going to do is go to deep seek.com
- back in N end looking at the credentials this is where you're going to put that API key you just generated this is where you're going to put that base URL that we just looked at in um deep seek docs and then finally the model right here will type in deep seek D Reasoner to access R1
- let's give this thing a try I'm going to say I want to create a few calendar events

**CTA / Outro:** "if you're looking to take your nidn and a automation skills a little bit farther and you'd like a more Hands-On approach then please check out my paid Community the link for that's also down in the description"

**Vocabulary:**
- DeepSeek
- R1
- tools agent
- prompt
- step-by-step plan of instructions
- calendar event
- email

**Analogies:** "think of this reasoning model as a really good planner"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:**
- [dollar_amounts] 2 bucks
- [dollar_amounts] 880,000 tokens
- [dollar_amounts] 14,000 tokens
- [dollar_amounts] 3 cents
- [percentages] 96% cheaper than using open AI a one reasoning model as well as being able to perform just as well as it or even better
- [time_references] 15 20 minutes
- [time_references] this morning
- [time_references] January 25th at 12:00 p.m. local time
- [time_references] 30 minutes before
- [named_tools] open router
- [named_tools] n8n

**Vulnerability:** "what I've been seeing is that this is just spinning and taking way way too long"

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] the first issue like I said you guys may be experiencing is calling it through open router where we are setting up a credential with the base URL of open router.
- [accelerate] if we want to connect to deep seek like this what you're going to do is go to deep seek.com
- [slow] So lately there's been a ton of hype around deep seeks new reasoning model deep seek R1 and this is because of the cost and performance which it's pretty much 96% cheaper than using open AI a one reasoning model as well as being able to perform just as well as it or even better

**Audience Language:** "you guys"

**Frameworks:**
- "So the first issue like I said you guys may be experiencing is calling it through open router where we are setting up a credential with the base URL of open router. aapi V1 we enter in the model name that's given to us in open router and we actually go to chat to this thing"
- "if we want to connect to deep seek like this what you're going to do is go to deep seek.com"
- "back in N end looking at the credentials this is where you're going to put that API key you just generated this is where you're going to put that base URL that we just looked at in um deep seek docs and then finally the model right here will type in deep seek D Reasoner to access R1"

---

## Video 202: Two Ways to Save 96% of Your Money Using DeepSeek R1 in n8n (23/01/25)
**Words:** 3558 | **Chunks:** 1

**Hook:** this is the riddle that we're going to send off to deep seek R1 and see if it can handle it you're in a room with three light switches each switch controls one of three light bulbs in a separate room but you can't see the light bulbs from where you are you can only enter the room with the light bulbs once how can you figure out which switch controls which bulb so we're going to send this riddle off to deep seek R1 right now it's thinking about the riddle it's going to assess its options and then it's going to tell us the result as well as all of the reasoning steps that it took in its brain to get to the answer

**Hook Type:** Demonstration

**Credential Drop:** NONE FOUND

**Signature Phrases:**
- "you're in a room with three light switches each switch controls one of three light bulbs"
- "so we're going to send this riddle off to deep seek R1 right now it's thinking about the riddle"
- "what's really cool is"
- "let me hit you with"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"

**Transitions:**
- "so let's jump into it"
- "if you want to check out this report I will leave the link for that in the description"
- "let me show you the way that right now I would start to implement deep seek R1 into my workflows"
- "what we're going to be doing is accessing deep seek R1 through an HTTP request where in here we're able to access the model and we're able to give it sort of a system prompt as well as an actual user prompt"
- "let's get back to the video"

**CTA / Outro:** "if you want to download this workflow you can do so for free by joining my fre School community that way you can just download it right away get this into your a into your NN environment and then you can just put in your API key and then you're good to go right away"

**Vocabulary:**
- deep seek
- riddle
- light switches
- light bulbs
- reasoning model
- n8n
- open router
- API key
- HTTP request
- model parameter

**Analogies:** "it's going to be super super simple you're going to go to deep seek.com you want to click up in the top right click on API platform"

**Curiosity Gaps:**
- "so let's jump into it and if you want to check out this report I will leave the link for that in the description"
- "if you've gotten there and you've you know con tried to connect open router to deep seek R1 or even deep seek V3 you you may have noticed some things about the way it's calling tools or the way that it's calling your vector database that maybe you weren't too happy with so let's talk about the right way to be using deep seek R1 in an"
- "let me show you the way that right now I would start to implement deep seek R1 into my workflows"

**Specificity:**
- [dollars] $60, $2.19
- [percentages] 96.4%
- [time_references] 23/01/25
- [named_tools] open router, n8n

**Vulnerability:** "I've also been experiencing this issue where I just want to say hello just to make sure that I'm actually connected"

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] discussing the riddle and solution, explaining how to set up deep seek R1 in n8n
- [slow] explaining the reasoning behind DeepSeek R1's approach

**Audience Language:** "you guys"

**Frameworks:**
- "as you can see we've got R1 01 another version of R1 that has different parameters 01 mini and then deep seek V3"

---

## Video 203: The Ultimate n8n Starter Kit (2025) (Free) (20/01/25)
**Words:** 845 | **Chunks:** 1

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

## Video 204: I Built a Team of Research Agents for Newsletter Automation in n8n (No Code) (19/01/25)
**Words:** 5231 | **Chunks:** 2

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

## Video 205: How I'd Teach a 10 Year Old to Build AI Agents (No Code, n8n) (17/01/25)
**Words:** 4506 | **Chunks:** 2

**Hook:** today I'm going to be walking through the simplest way to understand what an AI agent is the different components how they actually take action and do things and then I'm going to show you guys how to build a super simple one in minutes

**Hook Type:** Demonstration

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
- "you guys definitely helps me out"
- "let me know in the comments what else you guys want to see"
- "I really appreciate you guys making it see on this video"

**Transitions:**
- so once we get into NN and we're looking at the agent I'll break this down it'll make a little more sense
- finally of course it outputs something to us
- now if we go over here this is pretty much the agent we're going to be building today
- now that we see that the brain is working let's try to add some memory first
- now we need to add the tool and then after we add the tool we can configure the system message

**CTA / Outro:** let me know in the comments what else you guys want to see and I really appreciate you guys making it see on this video so I'll see you guys in the next one

**Vocabulary:**
- AI agent
- system prompt
- memory
- tool options
- large language model
- chat model
- session ID
- API key
- credential
- Google credentials
- really cool stuff
- basics
- enjoyed
- comments

**Analogies:**
- "so in the blue here we're looking at the actual AI agent and you can just think of this as kind of an entity a human um an employee anything that you can pretty much talk to"
- "the user message is the actual input this is how we're talking to the agent"
- "and then when you start to introduce tools this is where the magic really happens because now the large language model has the ability to actually take action"
- "so as far as this section of this little diagram input AI agent with a large language model memory system prompt and then outputting something this is like just kind of like a chat gbt thing that you would do um on your laptop or whatever and you're talking to it that's chat PT but then when you start to introduce tools this is where the magic really happens"
- "so as far as this section of this little diagram input AI agent with a large language model memory system prompt and then outputting something this is like just kind of like a chat gbt thing that you would do um on your laptop or whatever and you're talking to it that's chat PT but then when you start to introduce tools this is where the magic really happens"
- "so as far as this section of this little diagram input AI agent with a large language model memory system prompt and then outputting something this is like just kind of like a chat gbt thing that you would do um on your laptop or whatever and you're talking to it that's chat PT but then when you start to introduce tools this is where the magic really happens"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:** NOT FOUND

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] "so as you can see we have the input right here which is um on chat message received"
- [accelerate] "now that we have memory connected I'm going to say hi my name is Nate and it will say Hello nice to meet you Nate"
- [accelerate] "and then for two we're going to come in here and make this an expression this basically just means um rather than putting in a fixed email that would every single time this tool ran it would go to that email we want this to be dynamic so we're going to click on expression"
- [slow] "so as you can see right here we're looking at an AI agent sort of diagram with the different aspects"
- [slow] "then we also have instructions so instructions within an AI agent basically just to fine this is your role this is what you should be doing this is how you act these are the tools you have this is how you take action it's just it's commonly known known as a system prompt within a AI agent or a system message um not to be confused by user messages which is more of the actual input going in"
- [slow] "so we're going to chat with our agent in the naden environment so that's the user message coming through to the agent the agent uses the user message um along with its system message to understand um what do I need to do here"

**Audience Language:**
- "you guys"
- "those of you"
- "if you've been with me"
- "you guys"
- "what else you guys want to see"
- "I really appreciate you guys making it see on this video"

**Frameworks:**
- "today I'm going to be walking through the simplest way to understand what an AI agent is the different components how they actually take action and do things and then I'm going to show you guys how to build a super simple one in minutes"
- "so as far as this section of this little diagram input AI agent with a large language model memory system prompt and then outputting something"

---

## Video 206: How I Built A Technical Analyst AI Agent in n8n With No Code (17/01/25)
**Words:** 4047 | **Chunks:** 1

**Hook:** okay we have our AI agent right here ready to go waiting for an event in telegram so we're going to send off this text that asks it to analyze Apple

**Hook Type:** Demonstration

**Credential Drop:** NONE FOUND

**Signature Phrases:**
- "you're able to download this workflow for free"
- "let me hit you with"
- "what's really cool"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"

**Transitions:**
- okay so as far as the actual agent itself super super simple build
- now let's talk about how do we actually set up these post requests or sorry the one post request and the one get request because really that's the most difficult part of this workflow and still even that is not too difficult
- so now let's talk about how do we actually set up these post requests or sorry the one post request and the one get request because really that's the most difficult part of this workflow and still even that is not too difficult

**CTA / Outro:** "if you enjoy this one and it helps you out in some way you learned something new please give it a like definitely helps me out a lot"

**Vocabulary:**
- workflow
- telegram
- chart
- bearish
- macd
- candlestick
- analysis
- technical
- sentiment
- resistance

**Analogies:** "it's going into a little more detail about the patterns doesn't appear to be any strong reverse reversal Candlestick patterns like a hammer or dogee currently visible"

**Curiosity Gaps:**
- "so that's super cool and then finally it gives us some key takeaways and interpretation um we've got a bearish trend apple is currently in a short-term bearish Trend the consecutive red candlesticks and lack of reversal pattern suggests that this downward momentum might continue in the near term"
- "this analysis provides a snapshot of current market conditions but shouldn't be considered as Financial advice um this isn't really a financial adviser it's more of just giving a brief um financial analysis as well as a technical analysis on whatever stock you enter in there so I know I went over that feedback or sorry the analysis really really quick"
- "so now let's talk about how do we actually set up these post requests or sorry the one post request and the one get request because really that's the most difficult part of this workflow and still even that is not too difficult"

**Specificity:**
- [time_references] "17/01/25"
- [time_references] "back in NN"
- [time_references] "so now let's talk about how do we actually set up these post requests or sorry the one post request and the one get request because really that's the most difficult part of this workflow and still even that is not too difficult"
- [named_tools] "telegram"
- [named_tools] "chart image.com"
- [named_tools] "n8n"
- [named_tools] "anthropic 3.5"
- [named_tools] "git chart"
- [named_tools] "open AI analyze and image node"
- [named_tools] "nend"
- [named_tools] "my free school Community"
- [named_tools] "paid Community"
- [named_tools] "API key"

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] "so now let's talk about how do we actually set up these post requests or sorry the one post request and the one get request because really that's the most difficult part of this workflow and still even that is not too difficult"
- [accelerate] "so now let's talk about how do we actually set up these post requests or sorry the one post request and the one get request because really that's the most difficult part of this workflow and still even that is not too difficult"
- [slow] "okay so as far as the actual agent itself super super simple build"
- [slow] "so now let's talk about how do we actually set up these post requests or sorry the one post request and the one get request because really that's the most difficult part of this workflow and still even that is not too difficult"

**Audience Language:**
- "you're able to download this workflow for free"
- "let me hit you with"
- "what's really cool"
- "literally insane"
- "let's not waste any time"
- "honestly"
- "crazy"
- "insane"
- "wild"

**Frameworks:**
- "so as far as the actual agent itself super super simple build we've only got one tool which is the one that we created called get chart where we'll break that down after we talk about this initial agent but what's going on in here is we're communicating it with this agent through telegram so if I click into this trigger you can see that it's going to be on message received and all you need to get out of here is the telegram chat ID because when you're able to um link that ID to your window buffer memory you can see we we use that right here as well as um when we're actually sending information back both here and in the other workflow when we're sending that photo back into our telegram you need to reference that chat ID so that the um node knows what you know where to send this actual information so that's all we're doing as far as communication"
- "so now let's talk about how do we actually set up these post requests or sorry the one post request and the one get request because really that's the most difficult part of this workflow and still even that is not too difficult"

---

## Video 207: ElevenLabs Voice Agents Are So Easy to Build (No Code!) (15/01/25)
**Words:** 3783 | **Chunks:** 1

**Hook:** hey there I'm Archer what can I do for you

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
- so now that we've seen a quick demo
- let's take a quick look at what's going on in the super simple agent setup here
- first of all just within nadn whenever you're building an AI agent as you guys should know there's going to be an input and then that input's going to be fed into the agent
- so let's hop into 11 labs and start playing around with this stuff also a quick side note if you want to hop into this workflow check out the prompts play around with how I configured things
- back to the video so in 11 labs this is the email agent this is just the test environment where we're going to be talking to it to try things out

**CTA / Outro:** "as always if this one helped please leave a like definitely helps me out um I always really appreciate it and thanks for making it to the end of the video"

**Vocabulary:**
- super cool
- lunch tomorrow
- post request
- web hook node
- Google Sheets
- send email tool
- GPT 40
- AI agent
- email address
- subject and a body

**Analogies:**
- "it's basically Archer but with a different voice"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:**
- [time_references] 15/01/25
- [named_tools] 11 Labs
- [named_tools] N8n

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [accelerates] "so you want to send an email to Phil asking about a project update no problem I'll handle that"
- [accelerates] "all done it's been sent to Phil he'll be getting that email any minute"
- [accelerates] "could you actually go ahead and help me send another one of course I'm always happy to lend a hand or rather an email address who is this email for and what's it about just give me the details and I'll Whip It Up"
- [accelerates] "gotcha the email is on its way to Phil he'll be sure to see your invitation for lunch tomorrow"
- [slows] "so you want to send an email to Phil asking about a project update no problem I'll handle that"
- [slows] "all done it's been sent to Phil he'll be getting that email any minute"
- [slows] "could you actually go ahead and help me send another one of course I'm always happy to lend a hand or rather an email address who is this email for and what's it about just give me the details and I'll Whip It Up"
- [slows] "gotcha the email is on its way to Phil he'll be sure to see your invitation for lunch tomorrow"

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"
- "if you've been with me"

**Frameworks:**

---

## Video 208: Having an Actual Conversation with Data Using an ElevenLabs Voice Agent and n8n (13/01/25)
**Words:** 3153 | **Chunks:** 1

**Hook:** hey there I'm Eric what information are you looking for today

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
- so there was a quick demo of the project manager conversational voice agent that we're going to be breaking down today
- back to the agent so so um it's a super simple build as you can see within my AI agent here
- now let's look at what's actually going on within 11 Labs

**CTA / Outro:** if this one helped please leave a like um comment what other use cases you want to see with some voice agents and I really appreciate you guys making it all the way to the end I will see you guys in the next one thanks

**Vocabulary:**
- project manager
- voice agent
- vector database
- web hooks
- NADN
- 11 Labs
- AI chapot project

**Analogies:**
- "it's really not too complicated when you really break down and when you understand the fact that you could probably take this rag system that you already had built out this rag AI agent system and all you're doing is changing the input and changing the output and then you know exactly you're changing what's going on right here um what the agent's actually looking at as far as the input but that's really as simple as it needs to be"
- "it's like I said the same way that you would text it with telegram it would get your text it would search through the vector database it would think about how to respond it would create a response and then it would telegram you back it's the exact same process except for we're getting a query from 11 labs and then the agent is responding back to 11 Labs so that's how this is going to work"
- "you could hook up knowledge base but it would be a little bit more static so we want to use a vector database that it's going to be called through n at end because then we can update the vector database with some sort of automated pipeline rather than just having like um certain files in here right"

**Curiosity Gaps:**
- "I'll come back to this"
- "stay till the end"
- "here's where it gets interesting"

**Specificity:**
- [tools] Pine Cone
- [tools] NADN

**Vulnerability:** NONE FOUND

**Script Type:** LOOSE

**Energy Notes:**
- [accelerate] "it's really not too complicated when you really break down and when you understand the fact that you could probably take this rag system"
- [accelerate] "you could hook up knowledge base but it would be a little bit more static so we want to use a vector database that it's going to be called through n at end because then we can update the vector database with some sort of automated pipeline rather than just having like um certain files in here right"
- [slow] "so there was a quick demo of the project manager conversational voice agent that we're going to be breaking down today"
- [slow] "back to the agent so so um it's a super simple build as you can see within my AI agent here"
- [slow] "now let's look at what's actually going on within 11 Labs"

**Audience Language:**
- "you guys"
- "those of you"
- "OGs"
- "if you've been with me"

**Frameworks:**

---

