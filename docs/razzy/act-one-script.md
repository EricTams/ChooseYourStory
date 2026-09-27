# Razzy the Rogue — Act One script

All 34 screens have scene art. The story JSON is the source of truth.

A11: the prefect comes downstairs to fetch flour; Razzy remains in the kitchen. Voice choices identify both the voice and its apparent source. First two challenges keep failure first; later multi-choice scenes shuffle for readers, not in edit mode.

## A00 — Ready for the Dig

Scene: `meet_razzy`

Tomorrow is the Grand Archaeological Dig. Razzy has never been on a dig before, and he can hardly wait. What if he finds buried treasure?
He has everything ready. “I sure hope they choose me this time!”

- Go to the courtyard. → `below_the_noticeboard`

Illustration: Razzy sits on his bed buckling his packed adventure bag, a cleaning brush in its pocket and a small treasure pouch beside it. He looks up eagerly in the morning light.

[Art](../../game/data/stories/razzy-the-rogue/meet_razzy-packing.webp)

## A01 — Below the Noticeboard

Scene: `below_the_noticeboard`

Razzy runs up to the prefect. Will he get to dig with the older students?
“Have they chosen the digging team yet?”
“Not yet. Training first, then kitchen duty,” says the prefect. “Fetch a rope from upstairs.”
Kitchen duty again. Razzy wanted a chance to dig. Maybe if he does well at training, the teachers will choose him.

- Fetch your training rope. → `the_fast_way_down`

Illustration: Razzy reaches up for a kitchen-duty token while the prefect looks over him toward taller students beside the courtyard noticeboard.

[Art](../../game/data/stories/razzy-the-rogue/below_the_noticeboard.webp)

## A02 — The Fast Way Down

Scene: `the_fast_way_down`

Razzy has his rope. Training is about to start downstairs.
“Mind the luggage!” the prefect calls.
There is room to squeeze past it beside the wall. Razzy could also slide down the banister, but the laundry cart is near the bottom.

- Slide down the banister! → `express_delivery`
- Slip down beside the wall. → `down_the_stairs`

Illustration: Razzy pauses on the upper landing, looking down a sweeping banister past luggage; the prefect and laundry cart wait below.

[Art](../../game/data/stories/razzy-the-rogue/the_fast_way_down.webp)

## F01 — Express Delivery

Scene: `express_delivery`

Razzy slides too fast to stop.
“I've just folded those!” says the prefect.
“Sorry,” says Razzy. “Can you help me out?”

- Let's try that again. → `the_fast_way_down`

Illustration: Two orange ear tips and a striped tail protrude from rumpled sheets in the laundry cart as the prefect lifts a sheet.

[Art](../../game/data/stories/razzy-the-rogue/express_delivery.webp)

## A02b — Down the Stairs

Scene: `down_the_stairs`

Razzy squeezes past the luggage without knocking anything over.
“Slow down, Razzy!” calls the prefect.
“I want the first turn!” Razzy calls back, hurrying toward the lesson.

- Join the rope lesson. → `ropes_and_snares`

Illustration: Close view of Razzy eagerly stepping off the bottom stair with his rope. The prefect raises a paw beside the laundry cart. The luggage farther up the staircase is outside the main framing.

[Art](../../game/data/stories/razzy-the-rogue/down_the_stairs-v4.webp)

## A03 — Ropes and Snares

Scene: `ropes_and_snares`

Razzy wants to show the teacher how good he is with a rope.
The prefect pulls the dummy toward his loop. “Catch the dummy,” says the teacher. “Let the prefect pass first.”
The prefect steps into the loop. The dummy is just behind him. Razzy grips the rope, eager to pull.

- Pull now! → `wrong_adventurer`
- Wait for the dummy to enter the loop. → `a_quiet_success`

Illustration: The prefect pulls the wheeled dummy with a wooden handle, stepping into Razzy’s loose floor snare before the dummy reaches it. Razzy waits with the rope in his paws; the teacher watches.

[Art](../../game/data/stories/razzy-the-rogue/ropes_and_snares-v3.webp)

## F02 — Wrong Adventurer

Scene: `wrong_adventurer`

Razzy pulls too soon. The loop catches the prefect’s boot and trips him onto the mat.
“I am not the dummy!”
Razzy’s ears droop. “Sorry. I thought I could do it quickly.”

- Let's try that again. → `ropes_and_snares`

Illustration: The prefect sits sprawled on the mat with one boot caught in Razzy’s snare. The dummy is uncaught, its attached towing handle dropped on the floor. Razzy looks embarrassed.

[Art](../../game/data/stories/razzy-the-rogue/wrong_adventurer-v4.webp)

## A04 — Catching the Dummy

Scene: `a_quiet_success`

Razzy waits until the prefect is clear. When the dummy rolls into the loop, he pulls.
“Well done!” says the teacher. “You watched and waited.”
“I caught it!” Razzy beams. The teacher saw him do it, too. Perhaps he still has a chance to join the digging team.

- Go with the teacher to the hall. → `the_heavy_light`

Illustration: The snare catches the dummy’s front wheel and axle support. The prefect stands clear holding its wooden handle, while the teacher smiles at proud Razzy and gives him a thumbs up.

[Art](../../game/data/stories/razzy-the-rogue/a_quiet_success-v3.webp)

## A05 — The Chandelier

Scene: `the_heavy_light`

“Can you help me raise the chandelier?” asks the teacher.
Razzy takes the handle. He wants to do this himself, but it will not turn.
A small iron catch rests between the wheel’s teeth. Beside it, a stone weight hangs on a rope.

- Plant your paws and pull harder. → `going_nowhere`
- Lift the catch and turn the handle. → `lighter_than_it_looks`

Illustration: Razzy inspects a winch with a visible locking catch; lowered chandelier and counterweight establish the mechanism.

[Art](../../game/data/stories/razzy-the-rogue/the_heavy_light-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/the_heavy_light-v1.txt)

## F03 — Going Nowhere

Scene: `going_nowhere`

The handle will not move, however hard Razzy pulls.
“I thought I was strong enough,” he says.
“You are,” says the teacher. “Look at what’s holding the wheel.”

- Let's try that again. → `the_heavy_light`

Illustration: Razzy strains at the still-locked handle while the badger draws his attention to the catch. The chandelier remains low and the counterweight high.

[Art](../../game/data/stories/razzy-the-rogue/going_nowhere-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/going_nowhere-v1.txt)

## A06 — Lighter Than It Looks

Scene: `lighter_than_it_looks`

Razzy lifts the catch and turns the handle. The stone weight goes down and the chandelier rises.
“I can do it!”
“The weight helps,” says the teacher. “Now lower the catch to hold it there.”
Razzy checks that it is secure before letting go.

- Off to Potions. → `too_much_foam`

Illustration: Razzy smiles at the teacher beside the winch. The chandelier is raised overhead, the counterweight low, and the catch engaged again.

[Art](../../game/data/stories/razzy-the-rogue/lighter_than_it_looks-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/lighter_than_it_looks-v1.txt)

## A07 — A Little Too Much Foam

Scene: `too_much_foam`

Razzy wants to make paste for mending the expedition’s maps. His mixture starts to foam.
“Oh no. That’s much too much!”
He stops stirring, but the foam keeps rising. His spoon is stuck. A lid, a feather duster and a deep tray are within reach.

- Clamp the lid down. → `firmly_attached`
- Sweep it back with the feather duster. → `feathered_all_over`
- Slide the tray underneath. → `worth_keeping`

Illustration: Razzy considers the foaming pot and trapped spoon. A feather duster lies beside the lid at left; the deep tray waits at right. The hedgehog teacher watches.

[Art](../../game/data/stories/razzy-the-rogue/too_much_foam-v2.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/too_much_foam-v2.txt)

## F04 — Firmly Attached

Scene: `firmly_attached`

Razzy presses the lid down. Foam squeezes around its edge and sticks to his paws.
“It’s all over my paws!”
“Keep still,” says the teacher. “I have something to loosen it.”

- Let's try that again. → `too_much_foam`

Illustration: Razzy holds up his paws covered with sticky lavender foam; the lid lies tilted on the bowl and the spoon protrudes from beneath its edge. The teacher opens a small bottle to help.

[Art](../../game/data/stories/razzy-the-rogue/firmly_attached-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/firmly_attached-v1.txt)

## F10 — Feathers Everywhere

Scene: `feathered_all_over`

The duster sticks. Razzy gives it a hard tug—and flicks glue and feathers over himself.
“Please don’t tell the others,” he says.
The teacher reaches for the cleaning solution.

- Try again. → `too_much_foam`

Illustration: Razzy is coated in lavender glue and cream feathers, holding the nearly bare duster handle. The teacher holds cleaning solution beside the same pot, lid and tray.

[Art](../../game/data/stories/razzy-the-rogue/feathered_all_over-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/feathered_all_over-v1.txt)

## A08 — Clean It Up Later

Scene: `worth_keeping`

The tray catches the foam. Razzy breathes out. At last, it has stopped growing.
“Too sticky for maps,” says the teacher. “Take your pot with you. You can clean it after kitchen duty.”
Razzy sighs. Another job to do before he can pack.

- Head to kitchen duty. → `runaway_pumpkin`

Illustration: Razzy grips the tray containing his messy pot, looking disappointed as the teacher offers him a cleaning cloth. The foam is contained; there is no fresh jar.

[Art](../../game/data/stories/razzy-the-rogue/worth_keeping-v2.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/worth_keeping-v2.txt)

## A09 — The Runaway Pumpkin

Scene: `runaway_pumpkin`

Razzy leaves his sticky pot beside the kitchen basin.
“Help me pack for three days at camp,” says the cook.
The sack catches a pumpkin as she lifts it down.
“Razzy! Stop it!”
It’s heading straight for the cellar stairs. An empty hamper stands beside him.

- Catch it on the stairs! → `pumpkin_passenger`
- Tip the hamper into its path. → `an_extra_bun`

Illustration: The goose struggles to hold a sack lifted from the food shelf as the dislodged pumpkin bounces toward the cellar stairs. Razzy turns in alarm, with the empty hamper within reach. Neither choice has happened yet.

[Art](../../game/data/stories/razzy-the-rogue/runaway_pumpkin-v3.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/runaway_pumpkin-v3.txt)

## F05 — Pumpkin Passenger

Scene: `pumpkin_passenger`

Razzy tries to catch it on the stairs, but loses his footing.
“Are you hurt?” calls the cook.
“No,” he says. “I’m sorry about the pumpkin.”

- Let's try that again. → `runaway_pumpkin`

Illustration: At the foot of the cellar steps, Razzy sits unharmed beside a split pumpkin, with stringy pulp and seeds on his hood, paws and jacket. The cook looks down from the kitchen doorway, concerned.

[Art](../../game/data/stories/razzy-the-rogue/pumpkin_passenger-v2.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/pumpkin_passenger-v2.txt)

## A10 — An Extra Bun

Scene: `an_extra_bun`

The pumpkin rolls into the hamper and stops.
“I got it!” Razzy is pleased he could help.
“Quick thinking. Have a bun,” says the cook. She sends the rest upstairs on the serving lift.
“One each!” she calls up the shaft. Her voice echoes above.

- Listen to that echo. → `the_cook_upstairs`

Illustration: The pumpkin sits caught inside the sideways hamper. The cook offers delighted Razzy a bun; more buns wait on the serving lift behind them.

[Art](../../game/data/stories/razzy-the-rogue/an_extra_bun-v2.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/an_extra_bun-v2.txt)

## A11 — The Cook Upstairs

Scene: `the_cook_upstairs`

The prefect comes downstairs to fetch flour. He spots another bun.
“I think I’ll have that one too.”
Hidden under the table, Razzy has an idea. He can make his voice sound as though it’s coming from somewhere else. The prefect hasn’t seen him.

- Speak normally: “One each!” → `mind_your_own_buns`
- Make a monster’s voice come from the cupboard: “PUT THOSE BACK!” → `flour_from_nowhere`
- Make the cook’s voice come from upstairs: “One each!” → `a_voice_with_no_owner`

Illustration: The prefect holds a flour bowl and reaches for a bun at the right table. Razzy hides beneath it. A closed cupboard is at left and an open serving shaft is behind the prefect.

[Art](../../game/data/stories/razzy-the-rogue/the_cook_upstairs-v2.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/the_cook_upstairs-v2.txt)

## F06 — The Second Bun

Scene: `mind_your_own_buns`

“One each!” Razzy says in his own voice.
“Aren’t you meant to be working?” says the prefect, taking the bun.
Razzy frowns. The prefect never listens to him.

- Let's try that again. → `the_cook_upstairs`

Illustration: The prefect dismisses Razzy while holding the bun and level flour bowl. Razzy has emerged from under the right table, frustrated. The cupboard and serving hatch are unchanged.

[Art](../../game/data/stories/razzy-the-rogue/mind_your_own_buns-v2.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/mind_your_own_buns-v2.txt)

## F11 — The Cupboard Roars

Scene: `flour_from_nowhere`

Razzy makes a monster’s voice roar from the cupboard.
“PUT THOSE BACK!”
The prefect jumps and flings the flour.
“Cook! There’s something in your cupboard!”

- Try again. → `the_cook_upstairs`

Illustration: The prefect recoils looking left at the closed cupboard, accidentally tipping flour toward the right. Razzy is coated white beneath the table edge, orange ear tips and tail showing. The bun remains on the table.

[Art](../../game/data/stories/razzy-the-rogue/flour_from_nowhere-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/flour_from_nowhere-v1.txt)

## A12 — The Cook’s Voice

Scene: `a_voice_with_no_owner`

Razzy makes the cook’s voice come down the serving shaft.
“ONE EACH!”
“Sorry, Cook!” The prefect leaves the bun alone.
Razzy covers his mouth to keep from laughing. Then something flashes outside the kitchen window.

- Look out of the window. → `two_at_the_treeline`

Illustration: The prefect looks up into the serving shaft sheepishly, leaving the bun untouched and holding his flour bowl level. Razzy hides under the table, suppressing laughter.

[Art](../../game/data/stories/razzy-the-rogue/a_voice_with_no_owner-v2.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/a_voice_with_no_owner-v2.txt)

## A13 — Two at the Treeline

Scene: `two_at_the_treeline`

Razzy peers outside. A spyglass!
“Why are they watching our windows?”
He leans closer. The weasel lowers the spyglass, and both strangers hurry behind the trees. Now Razzy wants to know what they are doing.

- Look from the courtyard. → `suddenly_peddlers`

Illustration: Over Razzy’s shoulder through the kitchen window: the weasel uses a spyglass and the ferret peeks over the boundary wall. Both are outside the school grounds.

[Art](../../game/data/stories/razzy-the-rogue/two_at_the_treeline-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/two_at_the_treeline-v1.txt)

## A14 — Suddenly Peddlers

Scene: `suddenly_peddlers`

“Brushes and polish!” calls the weasel at the gate. “May we come in?”
Those are the same two strangers. Razzy is sure of it.
“We’re packing for tomorrow,” says the prefect. “We’re too busy.”
Razzy looks for the spyglass. Where have they hidden it?

- Watch what they do. → `counting_windows`
- Warn the prefect. → `too_busy_to_listen`

Illustration: Weasel makes an overpolite sales pitch as brushes fall from ferret's upside-down case; Razzy watches beside prefect.

[Art](../../game/data/stories/razzy-the-rogue/suddenly_peddlers-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/suddenly_peddlers-v1.txt)

## A15a — Counting Windows

Scene: `counting_windows`

Razzy stays quiet and listens.
“Will the kitchens be empty too?” asks the ferret.
“We could polish the floors while you’re away,” the weasel adds quickly.
That worries Razzy. He wants to tell someone who will listen.

- Tell Professor Burrowes. → `someone_who_listens`

Illustration: Razzy quietly examines a brush while listening. The weasel looks up toward the school, the prefect still blocking his path, while the ferret handles their sample case.

[Art](../../game/data/stories/razzy-the-rogue/counting_windows-v2.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/counting_windows-v2.txt)

## A16 — Someone Who Listens

Scene: `someone_who_listens`

“Come in, Razzy. What have you found?”
Burrowes puts down his brush and listens to the whole story. Razzy feels better already.
“I’ll look into it. Thank you for telling me.”
An old drawing catches Razzy’s eye. “Is that our school?”

- Ask about the drawing. → `the_missing_room`

Illustration: Burrowes sits at Razzy's eye level listening attentively; warm study and old drawing behind them.

[Art](../../game/data/stories/razzy-the-rogue/someone_who_listens-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/someone_who_listens-v1.txt)

## A17 — The Missing Room

Scene: `the_missing_room`

“Yes, before it was rebuilt,” says Burrowes. “Our founder had a private chamber. Nobody has found its entrance.”
“Could it still be there?”
“I hope so. I’ve wanted to find it for years,” says Burrowes.
Razzy leans closer. Imagine finding a room that even the teachers have never seen!

- Ask about tomorrow's dig. → `beside_the_luggage`

Illustration: Burrowes points to the outlined chamber in the old drawing as Razzy leans eagerly on the desk. The spare round spectacles remain in their open case.

[Art](../../game/data/stories/razzy-the-rogue/the_missing_room-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/the_missing_room-v1.txt)

## A18 — A Place Beside the Luggage

Scene: `beside_the_luggage`

“Am I on the digging team?” Razzy asks.
“Equipment group this time,” says Burrowes. “You’ll ride with me. I’ll check everyone aboard.”
Razzy looks down. He wanted to discover something, not carry it.
“Get some sleep,” says Burrowes. “We leave early.”

- Pack for morning. → `everybody_elses_adventure`

Illustration: Razzy holds his equipment-group tag, disappointed; Burrowes gestures warmly from his desk.

[Art](../../game/data/stories/razzy-the-rogue/beside_the_luggage-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/beside_the_luggage-v1.txt)

## A19 — Everybody Else’s Adventure

Scene: `everybody_elses_adventure`

Razzy cannot stop thinking about the lost room. If he finds it, perhaps the teachers will let him dig.
The founder’s tapestry shows the old school too. He could have one look before morning.
He waits until the others are asleep, then takes his bag.

- Examine the tapestry. → `the_moving_tapestry`

Illustration: Razzy sits awake on his bed beside his packed bag, watching the softly lit doorway. Other pupils sleep behind him.

[Art](../../game/data/stories/razzy-the-rogue/everybody_elses_adventure-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/everybody_elses_adventure-v1.txt)

## A20 — The Moving Tapestry

Scene: `the_moving_tapestry`

Razzy studies the school woven into the tapestry. Where could the entrance be?
The bottom of the cloth lifts. All the windows are shut.
He feels a draft behind it. His heart beats faster. There must be a gap somewhere.

- Pull the tapestry aside hard. → `founder_slightly_shorter`
- Crouch and follow the draft. → `the_ring_in_the_floor`

Illustration: Razzy notices tapestry hem lifting above a dusty floor while opposite windows remain shut.

[Art](../../game/data/stories/razzy-the-rogue/the_moving_tapestry-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/the_moving_tapestry-v1.txt)

## F07 — Caught in the Tapestry

Scene: `founder_slightly_shorter`

The tapestry falls from its hooks. Razzy freezes underneath it. Did anyone hear?
He tries to crawl out and bumps into the wall.
“Ow!” he whispers. “I should have been more careful.”

- Let's try that again. → `the_moving_tapestry`

Illustration: Founder tapestry drapes over Razzy with tiny orange feet protruding beneath it.

[Art](../../game/data/stories/razzy-the-rogue/founder_slightly_shorter-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/founder_slightly_shorter-v1.txt)

## A21 — The Ring in the Floor

Scene: `the_ring_in_the_floor`

Razzy follows the draft and finds an iron ring.
“A door!”
He pulls. The heavy hatch opens a little. What if this is the way to the lost room?
Then the worn stone beneath his paws begins to crack.

- Try to step back. → `nothing_beneath_his_paws`

Illustration: Razzy pulls a recessed iron ring to raise the hatch slightly; his hind paws rest on the worn stone lip beside it, where one small crack is beginning. Folded tapestry held aside.

[Art](../../game/data/stories/razzy-the-rogue/the_ring_in_the_floor-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/the_ring_in_the_floor-v1.txt)

## A22 — The Fall

Scene: `nothing_beneath_his_paws`

The edge of the opening crumbles. Razzy grabs for the floor, but his paws slip.
“Help!”
He falls into the dark, wishing he had told someone where he was going.

- Continue. → `beneath_the_school`

Illustration: Razzy falls beneath the crumbling rim of the opened hatch, reaching for the receding corridor light. A few small fragments fall beside him; the bottom remains unseen.

[Art](../../game/data/stories/razzy-the-rogue/nothing_beneath_his_paws-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/nothing_beneath_his_paws-v1.txt)

## A15b — Too Busy to Listen

Scene: `too_busy_to_listen`

“They were watching the school with a spyglass,” Razzy tells the prefect.
“We were looking at birds,” says the weasel.
Before Razzy can explain, someone calls for help with a trunk. “Tell Professor Burrowes,” says the prefect. “I have to go.”
Razzy wishes he had stayed.

- Tell Professor Burrowes. → `someone_who_listens`

Illustration: Razzy appeals to the distracted prefect as the weasel offers an innocent explanation. The ferret gathers brushes into the sample case.

[Art](../../game/data/stories/razzy-the-rogue/too_busy_to_listen-v1.webp) · [Prompt](../../game/data/stories/razzy-the-rogue/_prompts/too_busy_to_listen-v1.txt)
