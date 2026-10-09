# Builds the STRONGER cut of The Marketing Machine from src/base.html (a frozen copy of the live deck).
# The original deck/repo is never touched. Run:  python3 src/build_v3.py
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()
base = rd('src/base.html')
a = base.index('<div id="stage">') + len('<div id="stage">')
b = base.index('</div><!-- /stage -->')
head, mid, tail = base[:a], base[a:b], base[b:]

# ---------- split the original into numbered slides ----------
chunks = re.split(r'(?=<section )', mid)[1:]
S = {}
for i, c in enumerate(chunks, 1):
    S[i] = c[:c.rindex('</section>') + len('</section>')]
assert len(S) == 69, len(S)

def sub(n, old, new, count=1):
    s = S[n]
    assert old in s, (n, old[:60])
    S[n] = s.replace(old, new, count) if count else s.replace(old, new)

def notes(n, text):
    s = S[n] if isinstance(n, int) else n
    s = re.sub(r'(<script type="text/plain" class="notes">).*?(</script>)', lambda m: m.group(1) + text.strip() + m.group(2), s, flags=re.S)
    if isinstance(n, int): S[n] = s
    return s

def timer(html):
    return html.replace('<section ', '<section data-timer ', 1) if 'data-timer' not in html.split('>')[0] else html

NOTE = lambda t: '<script type="text/plain" class="notes">' + t.strip() + '</script>'

# =====================================================================================
# NEW SLIDES
# =====================================================================================

# --- 02 · the financial cost of an incomplete system (rec 1) ---
COST = '''<section class="slide wb s-cost" data-kicker="What an incomplete system costs">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a" style="font-size:84px">An incomplete marketing system<br>is the <em>most expensive</em> one.</h1>
    <p class="sub a" style="font-size:28px;margin-top:16px">Same ad. Same $1,000 spent. Same 100 leads. Only what happens after the click is different.</p>
    <div class="ccw a">
      <div class="ccx frag">
        <p class="n-k">Agent A</p><h3>Ads, then nothing</h3>
        <ul><li>Calls the next day</li><li>No reminders, so no-shows are gone</li><li>Not ready yet? Forgotten</li></ul>
        <div class="res"><b>2</b><span>clients</span><u>$1,388</u></div>
      </div>
      <div class="ccx g frag">
        <p class="n-k">Agent B</p><h3>Ads, plus the rest of the system</h3>
        <ul><li>Text in 1 minute, call in 5</li><li>Reminders, and a rebook text in minutes</li><li>Nurtured for 90 days</li></ul>
        <div class="res"><b>8</b><span>clients</span><u>$5,552</u></div>
      </div>
      <div class="cgap frag"><p class="n-k" style="color:#C7372F">Left on the table</p><div class="cg">$4,164</div><p>every 100 leads, for the agent who stopped at the ad.</p></div>
    </div>
    <p class="hand foot3 frag">most agents fix one of the five parts. usually the ads. <small>(example: $10 leads, $694 a client. the math comes later tonight.)</small></p>
  </div>
''' + NOTE('''
OPEN WITH THE MONEY, NOT THE AGENDA.

"Before I teach you anything, I want to show you what an incomplete system costs. Same ad. Same thousand dollars. Same hundred leads."

Reveal Agent A: calls the next day, no reminders, forgotten leads. Two clients, $1,388.
Reveal Agent B: text in a minute, call in five, reminders, ninety days of nurture. Eight clients, $5,552.

"The ad did not change. Four thousand one hundred sixty-four dollars of difference, on one hundred leads. That's what an incomplete system costs."

Then: "Most agents fix one of the five parts. Usually the ads. Tonight I'll show you all five."

These are the example numbers you'll see again on the five-numbers slide ($10 leads, $694 a client). Say "example" out loud.
''') + '\n</section>'

# --- 04 · receipts up front (rec 2) ---
RCPT = '''<section class="slide wb s-rcpt" data-kicker="Receipts first">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a" style="font-size:84px">The receipts, <em>up front.</em></h1>
    <p class="sub a" style="font-size:28px;margin-top:16px">Everything tonight comes out of accounts like these.</p>
    <div class="rcw a">
      <div class="rcc hi frag"><p class="n-k">An agent in the community</p><div class="big">$10,000</div><h3>In about six weeks</h3><p class="d">June to mid-July, <b>just by following the coaching</b>. Jill Coates, in her own words on the next slide.</p><span class="tag">Agent result</span></div>
      <div class="rcc frag"><p class="n-k">A client's ad account</p><div class="big">3,459<small> leads</small></div><h3>At $1.64 each</h3><p class="d">Last 30 days, Sep 6 to Oct 5, 2026. <b>$5,672.92 spent</b>, targeting veterans. I'll open the account later.</p><span class="tag">Lead cost</span></div>
      <div class="rcc frag"><p class="n-k">Our own ad account</p><div class="big">$5.92<small> per lead</small></div><h3>2,558 leads on $15,136</h3><p class="d">Webinars, Medicare Supplement and dental. <b>What a lead costs depends on who you talk to.</b></p><span class="tag">Lead cost</span></div>
    </div>
    <p class="hand foot3 frag">lead cost proves the ads. tonight I'll show you how a lead becomes a client.</p>
  </div>
''' + NOTE('''
PROOF IN THE FIRST FIVE MINUTES.

Three real things, in this order:
- Jill: ten thousand dollars in about six weeks, following the coaching. (Her full quote is the next slide.)
- A client's account: 3,459 leads at $1.64 over the last 30 days. $5,672.92 spent. Dates are on the slide.
- Our own account: 2,558 leads on $15,136, $5.92 average.

Be straight about what each one proves: "These two are lead cost. They prove the ads work. They don't prove revenue. That's why the second half of the night is about turning a lead into a client."

Saying that out loud is what makes the room believe the rest.
''') + '\n</section>'

# --- ads: every ad has a job (combines 15-19, rec 4) ---
JOB3 = '''<section data-part="3" class="slide wb s-job3" data-kicker="03 · Ads · Every ad has a job">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a" style="font-size:88px">Every ad has <em>a job.</em></h1>
    <p class="sub a">Stop asking “is this ad working?” Ask <b>what job it's doing</b>, then judge it by that.</p>
    <div class="j3w a">
      <div class="j3c t1 frag"><p class="n-k">Top · strangers</p><h3>Prospectors</h3><p class="tg">open the door</p>
        <ul class="ar"><li>Get <b>most of your budget</b></li><li>Reach <b>new people every day</b></li><li>Cost per lead <b>looks higher. That's normal.</b></li></ul>
        <div class="exad"><span>Example</span>“Turning 65 this year? There are 3 Medicare decisions to make first.”</div></div>
      <div class="j3c t2 frag"><p class="n-k">Middle · interested</p><h3>Warmers</h3><p class="tg">earn the next step</p>
        <ul class="ar"><li>Talk to people who <b>know they need a plan or an agent</b></li><li>They're <b>comparing</b> their options</li><li>Give them <b>a reason to pick you</b></li></ul>
        <div class="exad"><span>Example</span>“Plan G or Plan N? Join Thursday's 30-minute class and bring your questions.”</div></div>
      <div class="j3c t3 frag"><p class="n-k">Bottom · ready</p><h3>Closers</h3><p class="tg">book the call</p>
        <ul class="ar"><li>A <b>small budget, on purpose</b></li><li>Shown to <b>the same people again</b></li><li>Cost more to show, and <b>book the cheapest calls</b></li></ul>
        <div class="exad"><span>Example</span>“Ready to get your Medicare handled? Book a 15-minute call.”</div></div>
    </div>
  </div>
''' + NOTE('''
ONE SLIDE REPLACES FIVE. (Was: "stop asking", the funnel, prospectors, closers, talk where they are.)

"Stop asking 'is this ad working?' Ask 'what job is this ad doing?'"

Walk the three, one step each:
- Prospectors open the door. Strangers. Most of the budget. Their cost per lead looks higher, and that's normal.
- Warmers earn the next step. They know they need a plan, they're comparing.
- Closers book the call. Small budget on purpose, same people again, the cheapest booked calls.

Land it: "Same person, three different ads, depending on how much they already know."
''') + '\n</section>'

# --- ads: four numbers, one slide (combines 21-25, rec 4) ---
t = re.findall(r'<div class="tile \w+"><svg.*?</svg></div>', S[21], flags=re.S)
assert len(t) == 4, len(t)
FOURM = f'''<section data-part="3" class="slide wb s-4m" data-kicker="03 · Ads · Your numbers">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a" style="font-size:80px">Four numbers tell you <em>what an ad is doing.</em></h1>
    <div class="f4w a">
      <div class="f4c frag">{t[0]}<p class="n-k">01 · Spend</p><h3>Spend</h3><p class="hand">what Meta chooses</p><p class="r">The ad with the most money is the one Meta trusts. It's <b>usually your prospector.</b> Don't turn it off because its cost per lead looks high.</p></div>
      <div class="f4c frag">{t[1]}<p class="n-k">02 · CPM</p><h3>CPM</h3><p class="hand">who you reach</p><p class="r">What it costs to show your ad 1,000 times. <b>Low:</b> broad, cold, new people. <b>High:</b> warm people who know you. A high CPM on a closer is the design.</p></div>
      <div class="f4c frag">{t[2]}<p class="n-k">03 · Frequency</p><h3>Frequency</h3><p class="hand">where it sits in the funnel</p><p class="r">How many times one person sees it. Look <b>by the day</b>, not the month. <b>1.05</b> is brand-new people. <b>1.50</b> is people who know you.</p></div>
      <div class="f4c frag">{t[3]}<p class="n-k">04 · Cost per result</p><h3>Cost per result</h3><p class="hand">is it doing its job?</p><p class="r">Judge it <b>against the ad's job</b>, not against other ads. The number that pays you is <b>cost per booked call.</b></p></div>
    </div>
    <div class="f4ig frag"><p class="n-k">Ignore these for now</p><span class="c">Click-through rate</span><span class="c">Cost per click</span><span class="c">Hook rate</span><span class="c">Conversion rate</span><span class="c">ROAS</span></div>
  </div>
''' + NOTE('''
ONE SLIDE REPLACES FIVE. (Was: the four-metrics intro plus one slide each for spend, CPM, frequency and cost per result.)

"When you open your ad data, these are the four to look at first. Ignore the rest for now."

One breath per card:
- Spend: what Meta chooses. The top spender is usually your prospector. Don't kill it because the cost per lead looks high.
- CPM: who you reach. Low is cold and new. High is warm. A high CPM on a closer is the design.
- Frequency: where it sits in the funnel. By the day, not the month. 1.05 brand new, 1.50 people who know you.
- Cost per result: is it doing its job? The number that pays you is cost per booked call.

Then the next slide puts all four together on a real account.
''') + '\n</section>'

# --- ads: from lead cost to client cost (rec 6) ---
BRIDGE = '''<section data-part="3" class="slide wb s-brg" data-kicker="03 · Ads · From a lead to a client">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a" style="font-size:74px">A cheap lead isn't the goal.<br><em>A cheap client is.</em></h1>
    <div class="brw a">
      <div class="brh"><span>Cost per lead</span><span>Cost per booked call</span><span>Cost per client</span><span>A client is worth, day one</span></div>
      <div class="brr frag"><b>$1.64<small>client account · veterans</small></b><span class="v">$5.47</span><span class="v">$20.50</span><span class="v g">$694</span></div>
      <div class="brr frag"><b>$5.92<small>our account · blended</small></b><span class="v">$19.73</span><span class="v">$74.00</span><span class="v g">$694</span></div>
      <div class="brr ex frag"><b>$10.00<small>tonight's worked example</small></b><span class="v">$33.33</span><span class="v">$125.00</span><span class="v g">$694</span></div>
    </div>
    <p class="brn frag"><b>Example rates:</b> 30% book a call · 70% show up · 40% say yes = 8 clients per 100 leads. Cheaper leads often close at lower rates, so use your own. The five numbers come back in Part 5.</p>
  </div>
''' + NOTE('''
CONNECT THE LEAD NUMBERS TO BOOKED CALLS, CLIENTS AND MONEY.

"Those two accounts show lead cost. A lead isn't a client. Here's what the same lead costs by the time it's a booked call, and by the time it's a client."

Walk one row, slowly (the worked example): $10 a lead is $33 a booked call and $125 a client. Then: "And that client is worth $694 on day one, before the cross-sell."

Then say the caveat yourself: "These use example rates, 30% book, 70% show, 40% say yes. A $1.64 lead will not close like a $10 lead. Use your own numbers. We build the full version in Part 5."

Math check: cost per booked call = lead cost / 0.30. Cost per client = lead cost x 100 / 8.
''') + '\n</section>'

# --- the specialist: scope, capacity, turnaround (recs 7, 10) ---
SCOPE = '''<section class="slide wb s-scope" data-timer data-kicker="Your specialist · Exactly what that means">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a">Exactly what <em>“dedicated”</em> means.</h1>
    <div class="scw a">
      <div class="scc frag">
        <p class="n-k">What he does</p>
        <div class="scr"><i>Builds</i><div><b>Your campaign, end to end:</b> landing page, form, calendar, text and email follow-up, automations, tested.</div></div>
        <div class="scr"><i>How you ask</i><div>You send a request: <b>“I want to run a Part B delay campaign this month.”</b> He scopes it with you.</div></div>
        <div class="scr"><i>Turnaround</i><div><b>Ready to launch within 14 days</b> of kickoff.<span class="tbc">confirm</span></div></div>
        <div class="scr"><i>Revisions</i><div><b>Two rounds</b> of changes on each build.<span class="tbc">confirm</span></div></div>
      </div>
      <div class="scc no frag">
        <p class="n-k" style="color:#C7372F">What it isn't</p>
        <div class="scr"><i>Shared</i><div>Your specialist carries a <b>limited number of agents</b>, which is why only <span data-spots>12</span> join this week.</div></div>
        <div class="scr"><i>One at a time</i><div><b>One campaign build at a time.</b> Bigger projects are queued, not dropped.<span class="tbc">confirm</span></div></div>
        <div class="scr"><i>Not your ads</i><div>He builds the system around your ads. <b>Your ad spend and ad account stay yours.</b><span class="tbc">confirm</span></div></div>
        <div class="scr"><i>Not unlimited</i><div>It's a defined scope, not an on-call agency.</div></div>
      </div>
    </div>
    <div class="foot2 frag">Defined on purpose. <span>So there are no surprises after you join.</span></div>
  </div>
''' + NOTE('''
ANSWER "WHAT DOES DEDICATED MEAN?" BEFORE THEY ASK.

Left: what he builds, how you ask, how fast, how many revisions. Right: what it isn't.

"I'd rather be exact than impressive. Dedicated doesn't mean unlimited. It means a specialist with a limited number of agents, building one campaign at a time, to a clear scope."

BEFORE GOING LIVE (the yellow CONFIRM chips): these are drafts. Replace the turnaround, revisions and queue rules with your real internal scope. The chips disappear when you open the deck with ?live at the end of the URL.

Also confirm the open question on the Christopher slide: is every member's specialist Christopher himself, or his team? Say it the true way.
''') + '\n</section>'

# --- build demo (rec 5) ---
DEMO = '''<section class="slide wb s-demo" data-timer data-kicker="Your specialist · Watch it built">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a" style="font-size:78px">Watch it <em>get built.</em></h1>
    <p class="sub a" style="font-size:26px;margin-top:12px">A Part B delay campaign, from the request to ready-to-launch.<span class="tbc">placeholder recording · see notes</span></p>
    <div class="dmw a">
      <div class="frame live dmf"><div class="bar"><i></i><i></i><i></i><span>Your account · recorded build</span></div><video muted loop playsinline preload="auto" poster="assets/crm-workflows-poster.jpg" src="assets/crm-workflows.mp4" data-swap="assets/build-demo.mp4"></video></div>
      <div class="dml">
        <div class="st frag"><i>1</i><div><b>The request</b><span>“I want to run a Part B delay campaign.”</span></div></div>
        <div class="st frag"><i>2</i><div><b>Page and form built</b><span>On what converts for agents now.</span></div></div>
        <div class="st frag"><i>3</i><div><b>Calendar and follow-up wired</b><span>Texts, emails and reminders connected.</span></div></div>
        <div class="st ok frag"><i>✓</i><div><b>Tested, ready to launch</b><span>You review it, then go live.</span></div></div>
      </div>
    </div>
  </div>
''' + NOTE('''
SHOW IT, DON'T DESCRIBE IT. (New slide: a build demonstration.)

The video here is a PLACEHOLDER: a recording of the follow-up workflows inside the account. Replace it with the real thing:
1. Screen-record Christopher (or you) building one campaign: the request, the landing page and form, the calendar, the follow-up, the test. 60 to 120 seconds, sped up where it drags.
2. Save it as assets/build-demo.mp4 in this deck's folder. The slide switches to it by itself and the yellow chip disappears.

Better still, run it LIVE: have Christopher build a funnel on a shared screen while you take the first questions.

Talk over it: "This is what 'you say what you want, it gets built' looks like. Not a course. Not a ticket."
''') + '\n</section>'

# --- what you actually receive (rec 8; replaces the value stack) ---
RECV = '''<section class="slide wb s-recv" data-timer data-kicker="What you receive">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a" style="font-size:84px">Here's what you <em>actually receive.</em></h1>
    <div class="rvl a">
      <div class="rv star frag"><i>★</i><div><h3>Your first campaign, built and ready to launch</h3><p>By your specialist: landing page, form, calendar, text and email follow-up, automations.</p></div></div>
      <div class="rv frag"><i>01</i><div><h3>Your own GoHighLevel account, set up live with David</h3><p>A2P approved so texts land. Number, email and calendar connected.</p></div></div>
      <div class="rv frag"><i>02</i><div><h3>The funnels and automations I run, loaded in your account</h3><p>Webinar and lead-gen funnels, plus the texts and emails behind them: reminders, no-show recovery, 90-day follow-up.</p></div></div>
      <div class="rv frag"><i>03</i><div><h3>The Medicare Marketing Playbook</h3><p>Five chapters: market, message, ads, funnel, backend. Everything from tonight, step by step.</p></div></div>
      <div class="rv frag"><i>04</i><div><h3>The Skool community</h3><p>Every course unlocked on day one. A live call every business day.</p></div></div>
    </div>
    <div class="foot2 frag">Five things, delivered. <span>One person builds them.</span> I haven't told you the price yet.</div>
  </div>
''' + NOTE('''
REPLACES THE "VALUE SO FAR" RECAP. NO DOLLAR VALUES, JUST WHAT ARRIVES.

"Let me say it plainly. Here's what you actually receive."

Walk the five, the star first. Say each as a thing that shows up, not a thing that's "worth" something:
- Your first campaign, built and ready to launch, by your specialist.
- Your own GoHighLevel account, set up live with David, A2P approved.
- The funnels and automations I run, loaded in your account.
- The playbook, five chapters.
- The community, every course on day one, a live call every business day.

"I haven't told you the price yet." Don't say a number.
''') + '\n</section>'

# --- how can it be $300 (rec 8 / pasted critique) ---
HOW3 = '''<section class="slide wb s-how3" data-timer data-kicker="The honest answer">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a" style="font-size:88px">How can this be <em>$300 a month?</em></h1>
    <p class="sub a">Fair question. Here's the honest answer.</p>
    <div class="h3w a">
      <div class="h3c frag"><i>01</i><h3>Proven, not invented from scratch</h3><p>The funnels and automations are the ones already running in my own account. Your specialist adapts them to your business. He doesn't reinvent every one.</p></div>
      <div class="h3c frag"><i>02</i><h3>The teaching is built once</h3><p>The courses, the playbook and the live calls serve everyone in the group. They're built once and shared.</p></div>
      <div class="h3c frag"><i>03</i><h3>Capped capacity, defined scope</h3><p>Limited seats, and one defined build at a time, so every specialist can do real work. It's not an on-call agency.<span class="tbc">confirm</span></p></div>
    </div>
    <div class="h3f frag">Hire a specialist like this on his own and it's <b>$1,500 a month</b>: custom, open-ended work for one business. Here the scope is defined and the capacity is shared. <b>That's the trade.</b></div>
  </div>
''' + NOTE('''
ANSWER THE OBJECTION BEFORE THEY RAISE IT.

"You're probably thinking: how can you give me all of this for three hundred dollars a month? Fair. Here's the honest answer."

Three reasons, and say only what is true for your business:
1. Proven, not custom. The funnels are the ones running in your own account. The specialist adapts, he doesn't invent.
2. The teaching is built once. Courses, playbook and calls serve everyone.
3. Capped capacity and a defined scope. Limited seats, one build at a time. (Confirm the scope on the previous slide.)

Then the $1,500: "Hire a specialist like this alone and it's fifteen hundred a month, custom and open-ended, for one business. Here the scope is defined and the capacity is shared. That's the trade."

Source for the $1,500: Christopher's own booking page. Say it only if it's still true.
''') + '\n</section>'

# --- what happens after you join: scope, timeline, capacity, risk (rec 10) ---
PLAN = '''<section class="slide wb s-plan" data-timer data-kicker="Before you decide">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a">Exactly what happens <em>after you join.</em></h1>
    <div class="plw a">
      <div class="pls">
        <div class="pl frag"><i>Day 1</i><div><h3>Onboarding call with David</h3><p>Your account set up live, A2P approved, number, email and calendar connected.</p></div></div>
        <div class="pl frag"><i>Week 1</i><div><h3>Kickoff with your specialist<span class="tbc">confirm</span></h3><p>You choose the campaign. He scopes the build with you.</p></div></div>
        <div class="pl frag"><i>Day 14</i><div><h3>Built, tested, ready to launch<span class="tbc">confirm</span></h3><p>Landing page, form, calendar, follow-up and automations. You review it.</p></div></div>
        <div class="pl gold frag"><i>Then</i><div><h3>You launch</h3><p>With the playbook and a live call every business day behind you.</p></div></div>
      </div>
      <div class="plr">
        <div class="pb frag"><p class="n-k">Scope</p><h3>One campaign build at a time</h3><p>Two rounds of revisions. Your ad spend stays yours.<span class="tbc">confirm</span></p></div>
        <div class="pb frag"><p class="n-k">Capacity</p><h3><span data-spots>12</span> new members this week</h3><p>So every specialist carries a manageable number of agents.</p></div>
        <div class="pb frag"><p class="n-k">Risk</p><h3>Nothing up front. No contract.</h3><p>Cancel anytime.</p>
          <div class="tbc-block">Option: “Ready to launch in 14 days, or your next month is free.” A promise about delivery, not income. <span class="tbc">your call</span></div></div>
      </div>
    </div>
  </div>
  <div class="rail"><div class="p">$300<small>/mo</small></div><div class="d"></div><div class="u"><small>How to join</small>The link is in the chat.</div></div>
''' + NOTE('''
SCOPE, TIMELINE, CAPACITY AND RISK, BEFORE THE CLOSE. (Replaces "The outcome: your campaign, launched".)

Left, the timeline: Day 1 onboarding with David. Week 1 kickoff with the specialist. By day 14 built and ready to launch. Then you launch.
Right: scope (one build at a time, two revisions), capacity (twelve this week, and why), risk (nothing up front, no contract, cancel anytime).

"So you know exactly what you're agreeing to before you decide."

THE YELLOW CHIPS ARE DRAFT TERMS. Put in your real turnaround and revision limits, or delete the line. They hide when the URL ends in ?live.

THE DASHED BOX is an optional implementation guarantee ("ready to launch in 14 days or next month free"). It promises delivery, not income, which keeps it clear of Medicare income-claim problems. Use it only if you will honor it. Hidden with ?live either way, so decide, then remove or keep it in the file.

A2P approval depends on the carriers, not on you. Don't promise a date for it.
''') + '\n</section>'

# --- the break-even calculator (rec 9) ---
def fld(i, label, small, val, pre='', suf='', step='1'):
    pre_h = f'<em>{pre}</em>' if pre else ''
    suf_h = f'<em>{suf}</em>' if suf else ''
    return (f'<label><span>{label}<small>{small}</small></span>'
            f'<div class="fld">{pre_h}<input id="{i}" type="number" inputmode="decimal" min="0" step="{step}" value="{val}">{suf_h}</div></label>')

CALC = '''<section class="slide wb s-calc" data-timer data-kicker="Is $300 a month worth it?">
  <div class="light"></div>
  <div class="content">
    <h1 class="head a">Run the math with <em>your</em> numbers.</h1>
    <div class="calc a" id="calc">
      <div class="cin">
        <div class="pre"><p class="n-k">Start from</p><button type="button" data-p="cons" class="on">A cautious start</button><button type="button" data-p="ex">Tonight's example</button></div>
        ''' + fld('c-spend', 'Monthly ad spend', 'what you put into the ads', 1000, pre='$', step='50') \
            + fld('c-cpl', 'Cost per lead', 'tonight: $1.64 to $10', 12, pre='$', step='0.5') \
            + fld('c-book', 'Leads who book a call', 'example: 30%', 20, suf='%') \
            + fld('c-show', 'Booked who show up', 'example: 70%', 60, suf='%') \
            + fld('c-yes', 'Shown who say yes', 'example: 40%', 30, suf='%') \
            + fld('c-comm', 'Commission per client', 'first year. $694 = the Medicare Advantage example', 694, pre='$', step='10') \
            + fld('c-other', 'Other monthly costs', 'a VA, tools, anything else', 0, pre='$', step='50') + '''
        <label><span>This subscription<small>the community, the account and your specialist</small></span><div class="fix">$300</div></label>
      </div>
      <div class="cout">
        <div class="cfn"><div><b id="o-leads">0</b><span>Leads</span></div><div><b id="o-booked">0</b><span>Booked</span></div><div><b id="o-showed">0</b><span>Showed</span></div><div class="win"><b id="o-clients">0</b><span>Clients</span></div></div>
        <div class="cmn">
          <div class="row"><span>Commission from those clients</span><b id="o-rev">$0</b></div>
          <div class="row neg"><span>Ad spend</span><b id="o-spend">$0</b></div>
          <div class="row neg"><span>This subscription</span><b>−$300</b></div>
          <div class="row neg"><span>Other costs</span><b id="o-other">$0</b></div>
          <div class="row tot"><span>What's left this month</span><b id="o-net">$0</b></div>
        </div>
        <div class="cbe"><div><small>To cover your costs you need</small><b id="o-need">0</b></div><div><small>Which takes about</small><b id="o-leadsneed">0</b></div></div>
        <p class="cvd" id="o-verdict"></p>
      </div>
    </div>
    <p class="cfoot a"><b>What this leaves out:</b> your time, taxes, chargebacks, renewals and cross-sell (so it understates a good month), and the month or two before a new plan's commission is paid. Clients are rounded down at each step. The $2,000-a-client example needs a client who buys all four products, so it isn't the default here.</p>
  </div>
''' + NOTE('''
REPLACES "TWO CLIENTS. THAT'S THE WHOLE DECISION." THIS ONE SHOWS ITS WORK.

It's a live calculator. Click a preset or type your own numbers. Everything recalculates.

Start on "A cautious start" (a $12 lead, 20% book, 60% show, 30% say yes, $694 a client). With a $1,000 ad budget that comes out to about two clients, roughly break-even after the $300. Say so: "Even on cautious numbers, the first month roughly pays for itself. It doesn't make you rich. The upside is the backend."

Then click "Tonight's example" (the five numbers from Part 5). Eight clients, $5,552, about $4,250 left over.

Then change one number live, say the show rate. Let them see how fragile or strong it is.

DO NOT promise results. Say the line from the footer: it leaves out your time, taxes, chargebacks, renewals and cross-sell.

The answer to "is $300 worth it?" is a number they compute themselves: clients needed to cover the costs.

Clicks and keys on this slide don't advance the deck. Click anywhere outside the box to go on.
''') + '\n</section>'

# =====================================================================================
# EDITS TO EXISTING SLIDES
# =====================================================================================

# 45 · testimonials, now the second slide of the night
sub(45, 'data-kicker="Real members · Real results"', 'data-kicker="Real members · In their own words"')
notes(45, '''
PROOF, EARLY ON PURPOSE.

Moved up from the pitch. They should meet real agents before they hear a single price.

JILL: ten grand in about six weeks, following the coaching.
MINDY: started running Facebook ads, hired a VA, full calendar year-round. "Finally have a system to scale." That's the machine.
THOMAS: in his own words.

Keep it to thirty seconds. Then go to the bottleneck.
''')

# 57 · the execution gap, moved up to slide 6 (rec 3)
S[57] = S[57].replace('<section class="slide wb s-gap2" data-timer data-kicker="The one problem">', '<section class="slide wb s-gap2" data-kicker="The real bottleneck">')
sub(57, '<small>that\'s where agents get stuck.</small>', '<small>that\'s where agents stall. keep this slide in mind.</small>')
notes(57, '''
THE EXECUTION BOTTLENECK, EARLY. (Moved up from the pitch.)

"Here's the thing nobody says out loud. Most agents don't fail because they can't understand marketing. They fail between knowing what to do and getting it built."

Reveal the ten steps. You have the idea: that's step one of ten. Somebody has to build the page, the form, the pipeline, the calendar, the texts, the emails, the automations. Test it. Launch it.

"That's where agents get stuck. Keep this slide in mind. Tonight you'll learn what to build, and at the end I'll show you how it gets built."

DON'T SELL YET. This slide only plants the problem.
''')

# 1 and 3 had no notes in the original
S[1] = S[1].replace('</section>', NOTE('''
OPEN ON THE TITLE. NO SMALL TALK.

"Tonight is how to market a Medicare business, from the first ad to the renewal. Before I teach you anything, I want to show you what it costs when the system is incomplete."

Click.
''') + '\n</section>')
S[3] = S[3].replace('</section>', NOTE('''
WHO'S TALKING. TEN SECONDS.

"I was in the trenches like most of you. Started serving boomers in 2020. A hundred thirty-seven thousand in my first fifteen months, more than four thousand policies submitted. Now all I do is market, and train agents to market."

Then straight to the receipts.
''') + '\n</section>')
# 02 · frame
notes(2, '''
SET THE FRAME IN THIRTY SECONDS.

Say both things plainly. The room relaxes when they know where the pitch is.

"There's an offer at the end. I'll tell you when it's coming. Until then, this is marketing. Real marketing."

Then go. Don't linger.
''')

# 47 · chapter slide for the offer
sub(47, '<h1 class="a">How we help you <em>build it.</em></h1>', '<h1 class="a">Your Medicare Marketing Machine, <em>built with you.</em></h1>')
sub(47, 'The marketing, the system, and the person who builds it. Seven parts.', 'The education, the technology and the person who builds it.')
notes(47, '''
THE OFFER OPENS. THE 20-MINUTE CLOCK STARTS BY ITSELF ON THIS SLIDE (top right).

"I told you at the start there was an offer. Here it is. It's one thing: your Medicare Marketing Machine, built with you. The education, the technology, and the person who builds it."

Lead with the specialist next. Everything else supports him.
''')

# 58 · six people
notes(58, '''
SIX PEOPLE.

"Remember the ten steps from earlier. Now look at who has to do them. The agent, the media buyer, the funnel builder, the automation expert, the CRM admin, and tech support."

"You signed up for one of those."

Then, slowly: "So we solved that too." Click, and stop talking for a beat.
''')

# 59 · reveal: the specialist is the offer, not "Bonus #5"
S[59] = S[59].replace('data-kicker="Join today · Bonus 5 of 5"', 'data-kicker="Your specialist"')
sub(59, 'But today, we\'re adding one more thing', 'So here is the center of the offer')
sub(59, 'Bonus #5 · Only today', 'The part that gets it built')
sub(59, 'A specialist attached to your business.', 'A specialist attached to your business, who builds it.')
notes(59, '''
THE REVEAL. ALMOST NO TALKING.

"So here's the center of the offer."

Click. Wait two seconds.

"Your dedicated GoHighLevel specialist. Not a course. Not a support ticket. Not a Facebook group where you ask somebody how to do something. A specialist attached to your business, who builds it."

He is the offer. The community, the account and the playbook are what's behind him.
''')

# 60 · Christopher
S[60] = S[60].replace('data-kicker="Join today · Bonus 5 of 5"', 'data-kicker="Your specialist · Meet Christopher"')
notes(60, '''
MEET CHRISTOPHER.

"This is Christopher. He's the GoHighLevel specialist behind the Real Insurance Group."

"He's launched more than 800 webinar funnels. The webinar automation he built is running in over a thousand accounts. He runs GoHighLevel for six and seven-figure businesses. And he knows the insurance side, not just the software."

"A specialist like this costs fifteen hundred dollars a month, on its own."

JOHNNY, CONFIRM BEFORE GOING LIVE:
1. Is every member's dedicated specialist Christopher himself, or his team? Say it the true way.
2. "800+ webinar funnels" says little to a Medicare agent. If you can, add the number he has built specifically for insurance agents, and say it out loud here.
These numbers are from his booking page.
''')

# 61 · what he builds
S[61] = S[61].replace('data-kicker="Join today · Bonus 5 of 5"', 'data-kicker="Your specialist · What he builds"')
notes(61, '''
WHAT THE SPECIALIST BUILDS.

Left: "This is how it works. You say what you want. 'I want to run a Part B delay campaign this month.' Your specialist builds the landing page, the form, the calendar and the follow-up, and gets it ready to launch."

Right, walk the six: webinar funnels; landing pages and calendars; follow-up and automations; back-end systems; cross-sell and retention; old-lead reactivation.

"Every single thing I taught you tonight, built for you."

The chat on the left is an illustration. The next two slides make it concrete: a recorded build, then exactly what he does and doesn't do.
''')

# 48-50 · the community, now "behind your specialist"
S[48] = S[48].replace('<span class="mainpill a">How we help</span>', '<span class="mainpill a">Behind your specialist</span>')
notes(48, '''
BEHIND THE SPECIALIST: THE COMMUNITY.

"Behind your specialist is the Skool group. It's where you learn it, and where the wins happen."

"It helps you launch your first campaign, start to finish. It teaches you to cross-sell the book you already have, and to build a book of business that renews."

Talk over the video: "This is what you log into. Today."
''')

# 52-55 · bonuses become "included", no dollar values (rec 8)
def strip_values(n, k, also=None):
    S[n] = re.sub(r'<div class="stamp">.*?</div>', '', S[n], flags=re.S)
    S[n] = re.sub(r'<div class="bt frag">.*?</div>', '', S[n], flags=re.S)
    S[n] = re.sub(r'data-kicker="Join today · Bonus \d of 5"', f'data-kicker="Behind your specialist · {k} of 4"', S[n])
    S[n] = re.sub(r'Bonus #\d', f'Included #{k}', S[n])
    if also: S[n] = re.sub(r'<p class="also a">.*?</p>', f'<p class="also a">{also}</p>', S[n])
strip_values(52, 1, 'Behind your specialist, you also get')
strip_values(53, 2, 'And you also get')
strip_values(54, 3, 'And you also get')
strip_values(55, 4, 'And you also get')
sub(54, 'Typically a $1,000 setup. A one-on-one call with David', 'A one-on-one call with David')
sub(55, '<h1 class="head a">Medicare Automation <em>Snapshots.</em></h1>', '<h1 class="head a">Medicare Funnels &amp; <em>Automations.</em></h1>')
sub(55, 'The exact funnels running for me right now, refined on more than $100,000 of my own ad spend, loaded into your account.', 'The exact funnels running for me right now, refined on my own ad spend, loaded into your account.')
sub(55, '<b>Webinar snapshots</b>', '<b>Webinar funnel</b>')
sub(55, '<b>Lead gen snapshots</b>', '<b>Lead-gen funnels</b>')
sub(55, '<span class="g">Webinar snapshot</span>', '<span class="g">Webinar funnel</span>')
sub(55, '<span>Lead gen snapshot</span>', '<span>Lead-gen funnel</span>')
notes(52, '''
INCLUDED #1: THE MEDICARE MARKETING PLAYBOOK.

"Behind your specialist, you also get the Medicare Marketing Playbook. Tonight was the overview. The playbook is the whole thing, step by step: market, message, ads, funnel, backend."

Describe it as a thing that arrives. No dollar value.
''')
notes(53, '''
INCLUDED #2: YOUR GOHIGHLEVEL ACCOUNT.

"You also get your own GoHighLevel account. This is the back end for your ads. Remember speed to lead, nurture, reminders, the pipeline? This is where all of it lives."

You own the list. It's your account, your contacts.
''')
notes(54, '''
INCLUDED #3: ONBOARDING WITH DAVID.

"And you don't set it up alone. Meet David. He gets on a call with you, sets it up live, and gets everything connected."

Stop on A2P: "That's the registration that decides whether your texts land or silently die. None of the follow-up works without it."
''')
notes(55, '''
INCLUDED #4: THE FUNNELS AND AUTOMATIONS.

"And you get the funnels. The webinar funnel, registration, reminders and replay. The lead funnels. And every automation behind them, already built and loaded into your account."

(Renamed from "snapshots" so it doesn't sound like a free download.) The $100,000 ad-spend claim was removed; add it back only if it is true for these funnels.

Then go to the recap.
''')

# 51 · the gift, now just before the price
sub(51, 'Join on this webinar today, and you get every bonus I\'m about to show you. They\'re not on the website. They\'re not in the follow-up email. <b>They\'re only for the people here right now.</b>',
         'Join on this webinar today and everything we just walked through is yours. This offer isn\'t on the website. It isn\'t in the follow-up email. <b>It\'s only for the people here right now.</b>')
S[51] = S[51].replace('data-kicker="A gift for staying"', 'data-kicker="Because you stayed"')
notes(51, '''
THE GIFT. THIS IS WHERE THE PRICE IS ABOUT TO LAND.

THE CLOCK IS ALREADY RUNNING. It started on its own on the first offer slide. Point at it. (T pauses it, Shift+T resets it.)

"Because you stayed to the end, we have a special gift for you. If you join on this webinar today, everything we just walked through is yours."

"This offer isn't on the website. It isn't in the follow-up email. It's only for the people here right now. See the clock in the corner? It's already running. And we're only taking twelve people today. I'll tell you why in a minute."

Confirm all of that is true before you say it. Then the honest-answer slide.
''')

# 63 · price: one result, not five bonuses
S[63] = S[63].replace('<section class="slide wb s-offer" data-timer data-kicker="The price">', '<section class="slide wb s-offer" data-timer data-kicker="The price">')
sub(63, '<p class="lead a">The community, every bonus, and your specialist.</p>', '<p class="lead a">Your Medicare Marketing Machine, built with you.</p>')
sub(63, '<p class="all a">Nothing up front. No contract. Cancel anytime.</p>', '<p class="all a">No long-term contract · Cancel anytime · Nothing up front</p>')
sub(63, 'We teach you the Medicare marketing. We give you the software and the systems. And we give you the person who builds it. <b>Only on this webinar.</b>',
         'The education, the technology and the specialist who builds it, to launch and run a complete marketing system. <b>Only on this webinar.</b>')
notes(63, '''
THE PRICE. ONE RESULT, ONE NUMBER.

"Your Medicare Marketing Machine, built with you. Three hundred dollars a month. No long-term contract. Cancel anytime. Only on this webinar."

Then stop talking. Let the number sit.

JOHNNY: confirm the terms are true for the $300 version before going live (nothing up front, no contract, cancel anytime).
''')

# 64 · seats
sub(64, '<b>When the 12 are gone, the bonuses go with them.</b> Same as when the timer hits zero.', '<b>When the 12 are gone, this price and these onboarding slots go with them.</b> Same as when the timer hits zero.')
notes(64, '''
12 SEATS. REAL SCARCITY, WITH THE REAL REASON.

"We're only accepting twelve people today. That's our onboarding capacity this week: David sets up every account personally, live, one on one. And every one of you gets a real specialist, which only works if each one has a manageable number of agents."

"When the seats are gone, this price goes with them. Same as when that timer hits zero."

THE NUMBER MUST BE REAL. Change it in one place: the SPOTS line at the top of the deck script.

As people join during Q&A, call it out: "Two gone. Ten left."
''')

# 68 · AMA
sub(68, 'Seats and bonuses go in the order people join.', 'Seats go in the order people join.')
notes(68, '''
AMA. HALF THE SALES HAPPEN HERE.

Price and "the link is in the chat" stay on screen.

RULE: every answer ends "...and the link's in the chat."

Every three or four questions, flip back to the full-stack slide.

CALL THE SPECIALIST SPOTS as they go. Say names when people join.

Don't close the room when questions stop. The last two sales are the people still deciding.
''')

# 69 · final stack: deliverables, no dollar anchors (rec 8)
def fc(old_b, new_b):
    sub(69, old_b, new_b)
sub(69, '<b>$147<small>/mo</small></b>', '<b class="dv">Every course on day one. Live calls every business day.</b>')
sub(69, 'Bonus #1</p><h3>Medicare Marketing Playbook</h3><b>$3,000</b>', 'Included #1</p><h3>Medicare Marketing Playbook</h3><b class="dv">Five chapters, step by step.</b>')
sub(69, 'Bonus #2</p><h3>Your GoHighLevel Account</h3><b>$97<small>/mo</small></b>', 'Included #2</p><h3>Your GoHighLevel Account</h3><b class="dv">Yours, with your list.</b>')
sub(69, 'Bonus #3</p><h3>Onboarding with David</h3><b>$1,000</b>', 'Included #3</p><h3>Onboarding with David</h3><b class="dv">Set up live, A2P approved.</b>')
sub(69, 'Bonus #4</p><h3>Webinar + lead gen snapshots</h3><b>$5,000</b>', 'Included #4</p><h3>Funnels &amp; automations, built</h3><b class="dv">Loaded in your account.</b>')
sub(69, 'Bonus #5 · Only today</p><h3>Dedicated GoHighLevel Specialist</h3><b>$1,500<small>/mo</small></b>', 'The center</p><h3>Dedicated GoHighLevel Specialist</h3><b class="dv">Builds your first campaign.</b>')
sub(69, '<div><p class="k">Separately</p><div class="was">$9,000 + $1,744/mo</div></div>', '<div><p class="k">The result</p><div class="was res">Your campaign, built and launched</div></div>')
sub(69, '<p class="k">Today only</p>', '<p class="k">One price, only today</p>')
S[69] = S[69].replace('<h1 class="head a">Everything you get <em>if you join today.</em></h1>', '<h1 class="head a">Your Medicare Marketing Machine, <em>built with you.</em></h1>')
notes(69, '''
THE FULL STACK. LEAVE THIS UP FOR THE REST OF THE CALL.

This is the last slide. It stays on screen while you take questions, with the timer running in the corner.

Every few questions, walk it again: "Your specialist, who builds your first campaign. Behind him: the playbook, your own GoHighLevel account, onboarding with David, the funnels and automations already built, and the community. Three hundred dollars a month. Twelve people. The link is in the chat."

Call the count as people join: "Two gone. Ten left."
''')

# =====================================================================================
# ORDER
# =====================================================================================
order = [1, COST, 3, RCPT, 45, 57, 2, 4, 5] + list(range(6, 15)) + [JOB3, 20, FOURM, 26, 27, 28, BRIDGE, 29] \
      + list(range(30, 45)) + [46, 47, 58, 59, 60, 61, DEMO, SCOPE, 48, 49, 50, 52, 53, 54, 55, RECV, 51, HOW3, 63, CALC, 64, PLAN, 68, 69]
slides = [S[x] if isinstance(x, int) else x for x in order]
# every slide from the offer opener on carries the offer timer
start = order.index(47)
for i in range(start, len(slides)):
    if 'data-timer' not in slides[i].split('>', 1)[0]:
        slides[i] = slides[i].replace('<section ', '<section data-timer ', 1)
# the opener of the offer starts the clock
assert 'data-timer-start' in slides[start]
# nothing before the offer opener may carry the timer
for i in range(0, start):
    assert 'data-timer' not in slides[i].split('>', 1)[0], i

# =====================================================================================
# CSS, JS, TAIL
# =====================================================================================
css_end = head.index('</style>')
head = head[:css_end] + '\n' + rd('src/v11.css') + head[css_end:]
head = head.replace('<title>The Marketing Machine · Johnny Brock · The Real Insurance Group</title>',
                    '<title>The Marketing Machine · Johnny Brock · The Real Insurance Group (stronger cut)</title>')

# timer: 20 minutes (the pitch is longer now), friendlier labels
for old, new in (("DUR=15*60*1000", "DUR=20*60*1000"), ('<b>15:00</b>', '<b>20:00</b>'),
                 ("Tonight's bonuses are closed", "Tonight's offer is closed"), ("Tonight's bonuses end in", "Tonight's offer ends in"),
                 ('15-minute offer timer', '20-minute offer timer'), ('Start / pause the 15-minute offer timer (Shift+T resets). It starts itself on How we help.', 'Start / pause the 20-minute offer timer (Shift+T resets). It starts itself on the first offer slide.')):
    tail = tail.replace(old, new)
tail = tail.replace('</body>', '''<script>
/* stronger cut: ?live hides the yellow "confirm" chips and draft-only blocks */
if (new URLSearchParams(location.search).has('live')) document.body.classList.add('live');

/* demo slide: if assets/build-demo.mp4 exists, use it and drop the placeholder chip */
document.querySelectorAll('video[data-swap]').forEach(v => {
  fetch(v.dataset.swap, {method:'HEAD'}).then(r => {
    if (!r.ok) return;
    v.src = v.dataset.swap; v.removeAttribute('poster');
    const c = v.closest('.slide').querySelector('.tbc'); if (c) c.remove();
  }).catch(() => {});
});

/* break-even calculator */
(function(){
  const root = document.getElementById('calc'); if (!root) return;
  ['click','mousedown','keydown','keyup'].forEach(ev => root.addEventListener(ev, e => e.stopPropagation()));
  const g = id => root.querySelector('#' + id);
  const num = id => { const v = parseFloat(g(id).value); return isFinite(v) && v >= 0 ? v : 0; };
  const usd = n => (n < 0 ? '\\u2212' : '') + '$' + Math.abs(Math.round(n)).toLocaleString('en-US');
  const P = {
    cons: {spend:1000, cpl:12, book:20, show:60, yes:30, comm:694, other:0},
    ex:   {spend:1000, cpl:10, book:30, show:70, yes:40, comm:694, other:0}
  };
  const SUB = 300;
  function run(){
    const spend = num('c-spend'), cplRaw = num('c-cpl'), comm = num('c-comm'), other = num('c-other');
    const book = Math.min(num('c-book'), 100) / 100, show = Math.min(num('c-show'), 100) / 100, yes = Math.min(num('c-yes'), 100) / 100;
    const leads = cplRaw > 0 ? Math.floor(spend / cplRaw) : 0, booked = Math.floor(leads * book), showed = Math.floor(booked * show), clients = Math.floor(showed * yes);
    const rev = clients * comm, cost = spend + SUB + other, net = rev - cost;
    g('o-leads').textContent = leads.toLocaleString('en-US'); g('o-booked').textContent = booked.toLocaleString('en-US');
    g('o-showed').textContent = showed.toLocaleString('en-US'); g('o-clients').textContent = clients.toLocaleString('en-US');
    g('o-rev').textContent = usd(rev); g('o-spend').textContent = '\\u2212' + usd(spend); g('o-other').textContent = other ? '\\u2212' + usd(other) : '$0';
    const n = g('o-net'); n.textContent = (net > 0 ? '+' : '') + usd(net); n.className = net >= 0 ? 'pos' : 'neg';
    const need = comm > 0 ? Math.ceil(cost / comm) : null, rate = book * show * yes;
    g('o-need').innerHTML = need === null ? '\\u2014' : need + ' <em>client' + (need === 1 ? '' : 's') + ' a month</em>';
    const ln = (need !== null && rate > 0) ? Math.ceil(need / rate) : null;
    g('o-leadsneed').innerHTML = ln === null ? '\\u2014' : ln.toLocaleString('en-US') + ' <em>leads at these rates</em>';
    g('o-verdict').textContent = net >= 0
      ? 'At these numbers the month covers its costs and leaves ' + usd(net) + '. That is one month, before renewals.'
      : 'At these numbers you are short ' + usd(-net) + ' this month. Fix the show or close rate, or the cost per lead, before you raise the ad spend.';
  }
  function setPreset(k){
    const p = P[k];
    g('c-spend').value = p.spend; g('c-cpl').value = p.cpl; g('c-book').value = p.book; g('c-show').value = p.show;
    g('c-yes').value = p.yes; g('c-comm').value = p.comm; g('c-other').value = p.other;
    root.querySelectorAll('.pre button').forEach(b => b.classList.toggle('on', b.dataset.p === k));
    run();
  }
  root.querySelectorAll('.pre button').forEach(b => b.addEventListener('click', () => setPreset(b.dataset.p)));
  root.querySelectorAll('input').forEach(i => i.addEventListener('input', () => { root.querySelectorAll('.pre button').forEach(b => b.classList.remove('on')); run(); }));
  setPreset('cons');
})();
</script>
</body>''')

out = head + '\n\n<div id="stage">\n' + '\n\n'.join(slides) + '\n' + tail
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(out)
print('index.html', len(out), 'slides', out.count('<section '))
for must in ('$3,000', '$5,000', '$9,000', '$1,744', 'Bonus #', 'bonuses'):
    print(repr(must), out.count(must))
