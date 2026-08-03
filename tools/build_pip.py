#!/usr/bin/env python3
"""Rebuild pip-the-wizard-intro.json: punched-up text/choices, registry with
reference images, and LLMImageDescriptions assembled per docs/story-authoring.md.
Also emits prompt files and a generation manifest."""
import json, os

ROOT = '/Users/erictams/AIDev/ChooseYourStory'
STORY = f'{ROOT}/game/data/stories/pip-the-wizard-intro.json'
SLUG = 'pip-the-wizard-intro'
OUTDIR = os.path.dirname(os.path.abspath(__file__))
PROMPTS = f'{OUTDIR}/pip_prompts'
os.makedirs(PROMPTS, exist_ok=True)

d = json.load(open(STORY))
ART = d['artStyle']
LOC = d['locations']
# The branch must read as still growing from a tree, not floating loose over the water.
LOC['river']['description'] = "A fast-flowing river with rocky banks and a tall leaning riverside tree, one strong branch stretching out over the rushing water."
LOC['falls_overlook'] = {"description": "A winding foothill trail with a wide view of a tall mist-wrapped magical mountain, a great silver waterfall pouring down its face into the forest below."}

# ---------------- registry ----------------
CHARACTERS = {
    'pip': "A small round penguin wizard chick with black-and-white felted feathers, a little orange beak and orange feet, wearing a blue felt wizard robe and a tall floppy pointed blue wizard hat, both dotted with small yellow felt stars, and carrying a short wooden wand.",
    'teacher': "An elderly owl wizard with speckled brown-and-cream felted feathers, feathery ear tufts and bushy feather eyebrows, wearing long flowing grey wizard robes with wide sleeves.",
    'rival': "A young red fox wizard with russet fur, a white muzzle and a bushy white-tipped tail, wearing a fancy red felt robe with gold trim and a matching red pointed hat, with a smug, confident face.",
    'momma_bird': "A round little momma songbird with brown and rust-orange felted feathers, a sharp yellow beak, ruffled wings, and a fierce no-nonsense expression.",
    'phoenix': "A young phoenix chick with flame-colored felt plumage in reds, oranges and golds, a sweeping tail of ember-orange feathers, and little wisps of felted flame at its wingtips.",
    'troll': "A big lumpy grey-green troll with a huge round belly, long heavy arms, two small blunt tusks, small kind eyes, and a simple ragged brown cloth around its waist.",
    'unicorn': "A white unicorn with a soft cream felted mane and tail, a small golden spiral horn, and slender legs.",
}
ITEMS = {
    'bait_crystal': "A dazzling honey-gold teardrop-shaped crystal about the size of Pip's head, with many sharp sparkling facets, glowing warmly from within.",
    'big_crystal': "A huge dazzling pale-pink crystal, taller than Pip, with sharp bright facets, blazing with light.",
    'branch': "A strong straight living branch of pale wood, about as tall as Pip, with a few small green felt leaves near its tip.",
    'small_crystal': "A small clear crystal that fits in Pip's flipper, smooth and simple, glowing with a soft steady white light.",
}
NAMES = {
    'pip': 'Pip', 'teacher': 'the teacher', 'rival': 'Red Fox',
    'momma_bird': 'the momma bird', 'phoenix': 'the young phoenix',
    'troll': 'the troll', 'unicorn': 'the unicorn',
    'bait_crystal': 'the golden bait crystal',
    'big_crystal': 'the huge dazzling crystal', 'branch': 'the branch',
    'small_crystal': 'the small crystal',
}
REF_ORDER = ['pip', 'momma_bird', 'phoenix', 'rival', 'teacher', 'troll',
             'unicorn', 'bait_crystal', 'big_crystal', 'branch', 'small_crystal']
ORDINALS = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh',
            'eighth', 'ninth', 'tenth']
ALLDESC = {**CHARACTERS, **ITEMS}

# ---------------- punched-up text ----------------
TEXT = {
 'wyrm_or_worm': "Pip squeezes their eyes shut and pictures a fearsome dragon. Scales. Wings. Fire.\n\nA worm. Somehow, Pip pictures a worm.\n\nPOOF. In a puff of sparkles, Pip is a very small earthworm in a very large wizard hat. The teacher slowly raises one feathery eyebrow.",
 'a_birds_eye_view': "With a wobbling flourish, Pip casts the spell.\n\nThe teacher rises off the rug - up, up - hooting with delighted laughter. \"Oh my! Put me down, put me down. Well... maybe one more loop.\"\n\nWhen his talons touch the floor again, his eyes are twinkling. \"You're ready, Pip. Time for the next step in your studies.\"",
 'on_the_road': "\"A wizard's staff is not bought, Pip. It is gathered,\" the teacher calls. \"A branch for the body. A gift for the core. A crystal for the focus. Come home when all three have chosen you.\"\n\nPip grips their hat. A real staff. Real spells.\n\n\"And Pip - the forest rewards patience. Remember that, even when others forget it.\"",
 'into_the_forest': "Pip spots it right away: a strong living branch, green leaves, perfectly straight. The perfect staff base.\n\nThere is just one problem. Tucked between the twigs sits a neat little nest, and inside the nest rest three speckled eggs, warm and fragile.",
 'momma_bird_returns': "Pip's flipper barely brushes the bark when the sky explodes into feathers.\n\n\"CHEEP-CHEEP-CHEEEEP!\" Momma bird is home, and she is NOT happy about visitors.\n\nShe squawks. She flaps. She pecks Pip's hat right down over their eyes. Pip runs out of the clearing blind, arms waving, all the way back to the path.",
 'the_river_branch': "Pip finds another good branch - but it hangs far out over rushing water. The current roars and splashes below.\n\nPip's stomach flips. Climbing out there would be quick... and slippery, and soaked, and probably very splashy.\n\nOr Pip could slow down, breathe, and do this like a wizard.",
 'a_little_wet': "Pip scoots along the branch. So far so good.\n\nPip looks down. Not so good.\n\nThe river gives one big splash, the branch gives one little wiggle, and Pip's flippers give up entirely. SPLOOSH.\n\nPip drags themself back to shore looking like a very disappointed mop.",
 'the_grove': "Pip reaches a glowing grove - and stops short.\n\nRed Fox is there, gripping a frightened young phoenix and yanking out tail feathers one by one. \"Hold STILL,\" he snaps. \"My staff is going to be LEGENDARY, and legendary staffs need phoenix feathers.\"\n\nThe phoenix cries out. A loose feather drifts past Pip, glowing like an ember. It WOULD make an amazing core...",
 'scorched': "One feather. Surely the phoenix won't miss one little feather.\n\nPip reaches out - and the phoenix flares like a firework. WHOOMPH. It rockets skyward in a spray of sparks, gone.\n\nPip sits down hard, smoking gently. Beside them, Red Fox is smoking too. \"This,\" he coughs, \"is YOUR fault, waddle-wizard.\"",
 'into_the_grove': "Deeper in, the woods fork.\n\nFrom one direction echoes loud, sad crying from a dark cave. From the other, something large thrashes in a thicket.\n\nTwo sounds. Two someones. Pip can only help one first.",
 'the_troll': "Inside the cave, Pip finds a troll sitting on the stone floor, crying. One huge hand cradles a hugely swollen left cheek, and every whimper rattles pebbles off the walls.\n\n\"Hurts,\" the troll sniffles, in a voice like sad thunder. \"Tooth hurts SO MUCH.\"\n\nThe troll looks more miserable than scary. Mostly.",
 'troll_panics': "Pip tiptoes backward. A pebble crunches.\n\nThe troll's head snaps up. \"AAAH! TINY WIZARD!\" it bellows, scrambling for the wall.\n\nPip screams because the troll screamed. The troll screams because Pip screamed. Everyone screams all the way out of the cave.",
 'troll_gift': "POP! The bad tooth springs free - and the troll's sobs stop mid-sniffle.\n\nIt pokes its tongue into the brand-new gap and sighs a huge, relieved sigh. Then a slow, enormous smile spreads across its face.\n\nIt presses the tooth into Pip's flippers. \"For tiny dentist,\" it rumbles. \"Lucky tooth.\"",
 'the_unicorn': "Pip finds a unicorn tangled in thorny brambles, kicking and thrashing in a panic. Every kick pulls the vines tighter.\n\nPip takes one slow breath. Fast and flashy will only scare it more.\n\nProbably.",
 'unicorn_bolts': "The spell works perfectly. The thorns snap like harp strings.\n\nThe flash, however, works a little too well. The unicorn rockets into the trees, vines streaming behind it like party ribbons, gone before the sparkles land.\n\nPip lowers the smoking wand. \"You're welcome?\" they call, to nobody.",
 'unicorn_gift': "Pip works slowly. One burr. Then another. Then another.\n\nThe unicorn's breathing calms. By the last thorn, it is watching Pip with big quiet eyes.\n\nIt bows its head and offers a single shimmering strand of mane. Pip takes it like the treasure it is.",
 'the_waterfall': "Pip reaches the thundering waterfall - and there is Red Fox, soaked to the ears, wringing out his beautiful red robe.\n\n\"Not one word,\" he snarls. \"The waterfall cheated. It's WETTER than it looks.\"\n\nHe stomps off toward the trees, nose in the air. \"Enjoy getting soaked! I know a back way in. A legendary wizard always has a shortcut.\"",
 'the_bog': "The shortcut goes down, then squish, then squelch.\n\nSoon Pip is knee-deep in stinking bog mud, batting away a buzzing cloud of insects. There is no back way in. There is no Red Fox. There is only bog.\n\nSomewhere out there, Red Fox is just as muddy. That helps a little.",
 'behind_the_falls': "Pip holds their hat, hunches low, and pushes straight through the freezing spray - and out the other side into a hidden cavern.\n\nAhead the tunnel splits. One passage glitters with crystal dust, sparkling like it wants to be noticed. The other is dark, damp, and completely silent.",
 'collapsing_tunnel': "Up close, the glitter is fool's quartz - pretty, worthless, and holding the ceiling up.\n\nThe ceiling gives a warning rumble. Then it stops warning.\n\nPip sprints out with the tunnel crashing down behind them, coughing sparkly dust all the way back to the waterfall. Very glamorous. Very nearly flattened.",
 'fox_brag': "\"...and the ice wall?\" the voice echoes grandly around the cavern. \"I blasted right through it. Fireball! Fireball! WHOOSH. The mountain simply gave up.\"\n\nRed Fox is up on a ledge, telling the story to nobody at all, waving his paws for the fireball parts.\n\nPip goes very still. Fireballs... at an ice wall... holding back a mountain's worth of melted snow?\n\nThat does not sound clever. That sounds dangerous.",
 'the_crystal_chamber': "Red Fox stops mid-story. He does not have the decency to look even a little embarrassed.\n\n\"Took you long enough,\" he calls, pointing at the golden crystal over the pit. \"That one's the best one. I was saving it. But since you're here... bet you can't grab it, waddle-wizard.\"",
 'into_the_pit': "Pip jumps. For one glorious moment, Pip flies.\n\nThe crystal stays exactly where it is, and Pip does not.\n\nPip drops past it into the pit and lands with a thud, while Red Fox's laughter bounces around the chamber. \"Legendary!\" he howls. \"Do the flying part again!\"",
 'the_choosing': "On the chamber floor, Pip finds two crystals side by side.\n\nOne is huge and dazzling, humming with raw power, practically shouting 'pick me'. The other is small and clear, glowing softly, saying nothing at all.\n\nPip's flippers hover between them.",
 'shattered': "The big crystal hums louder as Pip reaches in - like it's excited. Like it's a little too excited.\n\nThe moment Pip touches it: CRACK.\n\nIt bursts into a thousand useless sparkles that rain down on Pip's hat. All that power, and it couldn't even hold itself together.",
 'the_flood': "Pip turns to leave - and finds Red Fox leaning in the tunnel mouth, arms crossed, smirking.\n\n\"That little pebble? THAT'S your focus? Well. Shortcut number two: nobody leaves until you hand it over.\"\n\nBehind him, a cracked wall of ice is leaking faster and faster - his shortcut went straight through it. Cold meltwater swirls around Pip's feet, and it is rising.",
 'cornered': "Pip shoves. Red Fox braces his legs against the tunnel walls and does not budge an inch.\n\n\"Nope,\" he says, ears just above the water. \"This is a toll tunnel now. One crystal to pass.\"\n\nThe water reaches Pip's chest. There is no more time to argue.",
 'swept_away': "The blast goes off like a firework in a bathtub.\n\nThe whole chamber sloshes, the current grabs Pip, and the crystal pops loose from their flippers - there it goes, twinkling away into the foam.\n\nThe waterfall spits Pip out at the bottom, empty-flippered and extremely rinsed.",
 'stuck_fast': "Pip picks the gap by Red Fox's elbow and wedges in. Halfway through, Pip stops. Not by choice.\n\n\"Comfy?\" asks Red Fox, slipping out the other way.\n\nMuch later, the momma bird finds Pip still stuck there. She does not say anything. She doesn't have to.",
 'crystal_in_hand': "Pip hugs the crystal tight, takes the biggest breath of their life, and dives.\n\nThe current does the rest - down, through, and out into the sunlight. Pip surfaces with the crystal held high.\n\nBehind the falls, Red Fox has discovered that blocking the only exit blocked his exit too. He will be yelling about it for a while.",
 'home_again': "Pip walks the last stretch of road home as the sun comes up, the finished staff humming softly in their flippers.\n\nThe teacher takes one look and his eyes go bright. \"A gathered staff. A chosen staff.\" He taps the floor with one wing. \"Now then - you owe me a levitation. This time, with your own staff.\"\n\nPip grins and raises it high.",
}

CHOICES = {
 'the_troll': [("Help pull the tooth.", "troll_toothpull"), ("Back away slowly.", "troll_panics")],
 'troll_gift': [("Bind it to the branch.", "core_tooth")],
 'unicorn_gift': [("Weave it into the branch.", "core_mane")],
 'into_the_forest': [("Take it - nest and all.", "momma_bird_returns"), ("Leave the nest be.", "the_river_branch")],
 'momma_bird_returns': [("Sorry, sorry, sorry!", "into_the_forest")],
 'the_river_branch': [("Scramble out and grab it!", "a_little_wet"), ("Breathe. Aim. Levitate.", "branch_in_hand")],
 'a_little_wet': [("Drip back onto the bank.", "the_river_branch")],
 'the_grove': [("Grab a feather for your staff.", "scorched"), ("Yell at Red Fox to stop!", "fox_toasted")],
 'troll_panics': [("Catch your breath. Head back.", "into_the_grove")],
 'unicorn_bolts': [("Back to the fork.", "into_the_grove")],
 'scorched': [("Pat out the sparks. Try again.", "the_grove")],
 'the_waterfall': [("Follow Red Fox's shortcut.", "the_bog"), ("Face the waterfall head-on.", "behind_the_falls")],
 'the_bog': [("Squelch back to the falls.", "the_waterfall")],
 'behind_the_falls': [("Follow the glitter.", "collapsing_tunnel"), ("Trust the quiet dark.", "crystal_cavern")],
 'crystal_in_hand': [("Put it all together.", "focus_bound")],
 'crystal_cavern': [("Look up.", "fox_brag")],
 'core_tooth': [("Onward to find the focus.", "mountain_falls")],
 'core_mane': [("Onward to find the focus.", "mountain_falls")],
 'collapsing_tunnel': [("Less glitter this time.", "behind_the_falls")],
 'the_crystal_chamber': [("Show him what a waddle-wizard can do!", "into_the_pit"), ("Ignore him. Search the chamber floor.", "the_choosing")],
 'into_the_pit': [("Climb out. Dust off.", "the_crystal_chamber")],
 'the_choosing': [("Grab the big loud one.", "shattered"), ("Take the small quiet one.", "crystal_chosen")],
 'shattered': [("Maybe the quiet one...", "the_choosing")],
 'the_flood': [("Shove past him!", "cornered"), ("Take a deep breath and dive.", "crystal_in_hand")],
 'cornered': [("Blast him out of the way!", "swept_away"), ("Squeeze through the gap by his elbow.", "stuck_fast"), ("Turn around. Take a deep breath and dive.", "crystal_in_hand")],
 'swept_away': [("Slog back up to the tunnel.", "cornered")],
 'stuck_fast': [("Wriggle free. Eventually.", "cornered")],
}

IMG_DESC = {
 'momma_bird_returns': "A furious momma bird squawking mid-air as Pip tumbles backward, hat knocked down over their eyes, flippers waving blindly.",
 'scorched': "The phoenix rockets skyward in a burst of flame, leaving both Pip and Red Fox sitting on the ground, singed and smoking.",
 'the_grove': "Red Fox plucks feathers from the crying phoenix while Pip stares longingly at a loose glowing feather drifting past.",
 'troll_panics': "The troll and Pip both scream - the troll scrambling for the back of the cave while Pip sprints out the front.",
 'the_waterfall': "Red Fox, soaked and scowling, wrings out his red robe by the waterfall while Pip watches from a boulder.",
 'the_flood': "Red Fox blocks the tunnel mouth, smirking, a cracked ice wall leaking behind him as meltwater rises around Pip.",
 'home_again': "Pip proudly holds the finished staff - branch and glowing crystal - before the beaming owl teacher.",
 'the_troll': "A large troll sits crying on the cave floor, one cheek hugely swollen, red and puffy, hand cradling it, big tears rolling down.",
 'collapsing_tunnel': "Pip sprints straight at the viewer, yelling, as the glittering tunnel caves in right behind them in a cloud of sparkly dust.",
 'stuck_fast': "Pip jammed tight in a narrow crack, feet kicking in the air, while the momma bird perches in front, wings on hips, glaring.",
 'troll_gift': "The troll, one fang newly missing from its grin, hands the long curved pulled fang to a proud Pip.",
}

# New scenes spliced in after their anchor scene (skipped if already present).
NEW_SCENES = [
    ('the_grove', 'fox_toasted', {
        'title': 'Toasted!',
        'text': "\"STOP!\" Pip's shout rings through the grove.\n\nRed Fox jumps, loses his grip, and the phoenix bursts free in a spray of sparks. It circles once over Pip's head - then turns on Red Fox with a WHOOMPH.\n\nWhen the smoke clears, Red Fox stands blinking, toasted from ears to tail. The phoenix settles onto a branch and gives Pip a small, warm nod.",
        'location': 'grove_entrance',
        'imageDescription': "The freed phoenix blazes overhead while Red Fox stands toasted and smoking; Pip watches, half triumphant, half wincing.",
        'LLMImageDescription': "",
        'image': f"data/stories/{SLUG}/fox_toasted.png",
        'choices': [{'text': "Leave him to smolder.", 'target': 'into_the_grove'}],
    }),
    ('the_troll', 'troll_toothpull', {
        'title': 'The Big Pull',
        'text': "\"Open wide,\" says Pip, \"and hold very still.\"\n\nPip's wand glows. A rope of sparkly magic loops around the sore tooth. Pip digs in their heels and leans back with all their might.\n\nThe tooth wiggles. The troll's eyes cross. The whole cave holds its breath.",
        'location': 'troll_cave',
        'imageDescription': "Tiny Pip leans back hauling on a glowing rope of magic looped around the troll's sore tooth while the troll's eyes cross.",
        'LLMImageDescription': "",
        'image': f"data/stories/{SLUG}/troll_toothpull.png",
        'choices': [{'text': "PULL!", 'target': 'troll_gift'}],
    }),
    ('troll_gift', 'core_tooth', {
        'title': 'The Lucky Core',
        'text': "\"A gift for the core,\" Pip whispers.\n\nPip lays the branch across two stones and sets the troll's tooth against the middle of the wood. The wand glows. Slowly, gently, the tooth sinks in, like a stone into honey.\n\nThe whole branch hums once, deep and happy. The lucky tooth is home.",
        'location': 'troll_cave',
        'imageDescription': "Pip guides the glowing troll tooth as it sinks into the middle of the branch, wand raised.",
        'LLMImageDescription': "",
        'image': f"data/stories/{SLUG}/core_tooth.png",
        'choices': [{'text': "Onward to find the focus.", 'target': 'mountain_falls'}],
    }),
    ('behind_the_falls', 'crystal_cavern', {
        'title': 'The Crystal Cavern',
        'text': "The dark tunnel opens, and Pip forgets to breathe.\n\nCrystals glow from every wall of a huge cavern. In the middle of the floor yawns a deep, dark pit - and high above it, one golden crystal dangles from a single root, turning slowly.\n\nThen a familiar voice drips down from somewhere up high.",
        'location': 'crystal_chamber',
        'imageDescription': "Pip stands tiny at the tunnel mouth of a vast glowing crystal cavern, a golden crystal dangling high above the central pit.",
        'LLMImageDescription': "",
        'image': f"data/stories/{SLUG}/crystal_cavern.png",
        'choices': [{'text': "Look up.", 'target': 'the_crystal_chamber'}],
    }),
    ('crystal_in_hand', 'focus_bound', {
        'title': 'The Focus',
        'text': "\"A crystal for the focus,\" Pip whispers.\n\nPip lays the staff on a flat stone beside the pool and sets the small crystal at its tip. The wand glows. The pale wood curls around the crystal like fingers closing, and it settles in with a soft, clear chime.\n\nThe staff is finished. It hums like it has always been whole.",
        'location': 'waterfall_base',
        'imageDescription': "By the waterfall pool at dawn, the small crystal settles into the tip of Pip's staff inside a ring of soft light.",
        'LLMImageDescription': "",
        'image': f"data/stories/{SLUG}/focus_bound.png",
        'choices': [{'text': "Home to the teacher.", 'target': 'home_again'}],
    }),
    ('unicorn_gift', 'core_mane', {
        'title': 'The Silver Core',
        'text': "\"A gift for the core,\" Pip whispers.\n\nPip lays the branch across two stones and presses the shimmering strand along the middle of the wood. The wand glows. The hair winds itself around the branch in a silver spiral - then sinks beneath the bark.\n\nThe whole branch hums once, soft and bright. The unicorn's gift is home.",
        'location': 'thicket',
        'imageDescription': "A silver strand of unicorn mane winds itself around the branch in a glowing spiral as Pip casts.",
        'LLMImageDescription': "",
        'image': f"data/stories/{SLUG}/core_mane.png",
        'choices': [{'text': "Onward to find the focus.", 'target': 'mountain_falls'}],
    }),
    ('crystal_cavern', 'fox_brag', {
        'title': 'Fireball! Fireball!',
        'text': "\"...and the ice wall?\" the voice echoes grandly around the cavern. \"I blasted right through it. Fireball! Fireball! WHOOSH. The mountain simply gave up.\"\n\nRed Fox is up on a ledge, telling the story to nobody at all, waving his paws for the fireball parts.\n\nPip has never once seen Red Fox make a fireball.",
        'location': 'crystal_chamber',
        'imageDescription': "Close-up of Red Fox mid-brag, chest puffed, beneath a big thought bubble of himself heroically flinging fireballs at an ice wall.",
        'LLMImageDescription': "",
        'image': f"data/stories/{SLUG}/fox_brag.png",
        'choices': [{'text': "Ahem.", 'target': 'the_crystal_chamber'}],
    }),
    ('the_choosing', 'crystal_chosen', {
        'title': 'The Quiet One',
        'text': "Pip lifts the small crystal in both flippers.\n\nIt is light, and cool, and its glow is perfectly steady - no flicker, no hum, no showing off. It simply shines, like it could hold all the power in the world and never once crack.\n\nPip grins. This is the one.",
        'location': 'crystal_chamber',
        'imageDescription': "Close-up of Pip beaming, holding the small crystal up in both flippers, its steady white glow lighting their face.",
        'LLMImageDescription': "",
        'image': f"data/stories/{SLUG}/crystal_chosen.png",
        'choices': [{'text': "Time to head home.", 'target': 'the_flood'}],
    }),
    ('core_mane', 'mountain_falls', {
        'title': 'The Silver Falls',
        'text': "The forest opens, and there it is at last: the mountain.\n\nIt rises over the treetops wrapped in mist, and down its face pours a great silver waterfall, glittering like a ribbon of starlight.\n\nSomewhere behind all that falling water, a crystal is waiting. Pip squares their shoulders and starts up the trail.",
        'location': 'falls_overlook',
        'imageDescription': "A wide vista: tiny Pip on the foothill trail, gazing up at a mist-wrapped magical mountain with a silver waterfall pouring down its face.",
        'LLMImageDescription': "",
        'image': f"data/stories/{SLUG}/mountain_falls.png",
        'choices': [{'text': "Climb to the falls.", 'target': 'the_waterfall'}],
    }),
]
for anchor, sid, payload in NEW_SCENES:
    if sid in d['scenes']:
        continue
    spliced = {}
    for k, v in d['scenes'].items():
        spliced[k] = v
        if k == anchor:
            spliced[sid] = payload
    d['scenes'] = spliced

# ---------------- scene image specs ----------------
# blocks: ('std', id, action) -> "Name, matching the Nth reference image — desc — action"
#         ('raw', text)       -> inserted verbatim
S = {
 'opening': dict(refs=['pip','teacher'], blocks=[
    ('std','pip',"stands in the middle of the small rug at the center of the study, wand raised, flippers trembling slightly, eyes wide with nervous determination."),
    ('std','teacher',"stands to one side, watching Pip closely, patient and expectant.")],
    extra="Pip is the one casting; the teacher only watches. Do not swap their roles.",
    light="Warm candlelit evening light."),
 'wyrm_or_worm': dict(refs=['pip'], blocks=[
    ('raw',"In the middle of the small rug sits a tiny pink felted earthworm wearing Pip's oversized blue wizard hat dotted with yellow felt stars - the same hat as the first reference image - the hat far too big for it, with a tiny startled felt face peeking out from under the brim and a few leftover magic sparkles drifting down around it.")],
    extra="The worm is small in the frame, alone on the rug.",
    light="Warm candlelit evening light.",
    dev="Deliberate deviation from the first reference: Pip has accidentally transformed into an earthworm - only the oversized hat matches the reference."),
 'a_birds_eye_view': dict(refs=['pip','teacher'], blocks=[
    ('std','teacher',"floats in mid-air above the rug, wings half-spread, hooting with delighted laughter, grey robes drifting around him."),
    ('std','pip',"stands below on the rug, wand raised toward the teacher, face lit up with relief and pride.")],
    extra="The teacher is the one floating; Pip stays on the ground casting. Do not swap their roles.",
    light="Warm candlelit evening light."),
 'on_the_road': dict(refs=['pip','teacher'], blocks=[
    ('std','pip',"walks away down the winding dirt path in the foreground, a small travel satchel over one shoulder, looking ahead with excited determination."),
    ('std','teacher',"stands small in the background at the start of the path, one wing raised in a warm wave goodbye.")],
    extra="Pip walks away in the foreground; the teacher stays behind in the background waving.",
    light="Bright early-morning light."),
 'into_the_forest': dict(refs=['pip'], blocks=[
    ('std','pip',"stands at the base of the big leafy tree, looking up longingly at a strong straight branch; tucked between the twigs of that branch sits a tidy nest holding three small speckled felt eggs.")],
    light="Soft sunlit afternoon light."),
 'momma_bird_returns': dict(refs=['pip','momma_bird'], blocks=[
    ('std','momma_bird',"bursts through the air just above Pip, wings spread wide, beak open in a furious squawk, a few loose feathers flying."),
    ('std','pip',"tumbles backward away from the tree, wizard hat knocked down over their eyes, flippers waving blindly.")],
    extra="The momma bird is the one attacking; Pip is fleeing. Do not swap their roles.",
    light="Soft sunlit afternoon light with a couple of loose leaves in the air."),
 'the_river_branch': dict(refs=['pip','branch'], blocks=[
    ('std','branch',"grows from the tall leaning riverside tree, still attached to the trunk, stretching far out over the rushing water with its leafy tip dangling above the current."),
    ('std','pip',"stands on the rocky bank hugging their own flippers, looking out at the branch with a worried face.")],
    light="Cool bright daylight with white spray above the rapids."),
 'a_little_wet': dict(refs=['pip','branch'], blocks=[
    ('std','branch',"grows from the tall leaning riverside tree, still attached to the trunk, stretching out over the rushing water."),
    ('std','pip',"clings to the branch out over the river, eyes wide with panic, one flipper slipping free, a big splash of water rising just below them.")],
    light="Cool daylight, water spray everywhere."),
 'branch_in_hand': dict(refs=['pip','branch'], blocks=[
    ('std','branch',"floats gently down into Pip's flippers, wrapped in a faint soft magical glow."),
    ('std','pip',"stands safely on the bank catching the branch in both flippers, beaming with pride.")],
    light="Warm late-day light on the riverbank."),
 'the_grove': dict(refs=['pip','phoenix','rival'], blocks=[
    ('std','rival',"stands in the middle of the grove behind the phoenix, holding it still with one paw on its back while the other paw grips the phoenix's long trailing tail plumes, pulling them taut mid-yank, mouth open mid-snap, annoyed. He pulls from the TAIL only - both wings are free and untouched."),
    ('std','phoenix',"faces away from Red Fox, straining forward with both wings flapping free, its long ember tail feathers stretched back toward the fox's fist, beak open in a frightened cry, a couple of loose tail plumes drifting to the moss."),
    ('std','pip',"stands at the edge of the grove in the foreground, staring longingly at a loose glowing tail feather drifting past at eye level, one flipper half-raised toward it, visibly torn. Pip's other flipper holds one single short straight wooden wand pointed down at their side - just one plain straight stick, not bent, not crossed, not forked.")],
    extra="Red Fox is the one gripping the phoenix; Pip only watches from the edge, tempted by the drifting feather. Do not swap their roles.",
    light="Soft magical dusk glow from the luminous moss."),
 'scorched': dict(refs=['pip','phoenix','rival'], blocks=[
    ('std','phoenix',"bursts upward in a bright flare of felted flame, rocketing toward the sky trailing sparks."),
    ('std','pip',"sits flat on the ground where the blast knocked them, robe singed and smoking gently, eyes wide and startled."),
    ('std','rival',"sits on the ground a short distance from Pip, equally scorched - fancy red robe singed, hat tip charred - coughing out a little puff of grey smoke while glaring sideways at Pip.")],
    extra="Both Pip and Red Fox are singed and sitting on the ground; the phoenix escapes upward. Do not add any other characters.",
    light="Hot orange flare light from the phoenix against the dusk glow.",
    dev="Deliberate deviation: both Pip's and Red Fox's clothes are scorched and smoking - otherwise they match their references."),
 'fox_toasted': dict(refs=['pip','phoenix','rival'], blocks=[
    ('std','phoenix',"hovers overhead with wings spread wide, blazing proudly and free, a few sparks still drifting down."),
    ('std','rival',"stands stiff, toasted from ears to tail - fur sooty, fancy red robe scorched at the edges, hat charred and drooping, a little puff of grey smoke rising off him. His usual smug grin is gone: he is scowling, eyebrows knotted, mouth a flat grumpy line, ears tilted back, thoroughly annoyed."),
    ('std','pip',"stands in the foreground looking up at the phoenix, half triumphant, half wincing.")],
    extra="Red Fox is the toasted one; Pip is untouched. The phoenix flies free and is not held by anyone. Do not swap their roles.",
    light="Bright warm flare-light fading into the dusk glow, sparks drifting.",
    dev="Deliberate deviation: Red Fox is scorched, sooty and smoking, and his expression is annoyed rather than smug - otherwise he matches his reference."),
 'into_the_grove': dict(refs=['pip'], blocks=[
    ('std','pip',"stands at the fork, head tilted as they listen, looking between the dark cave mouth on one side and the thorny thicket on the other.")],
    light="Dim forest light."),
 'the_troll': dict(refs=['pip','troll'], blocks=[
    ('std','troll',"sits on the lumpy stone floor crying, one huge hand cradling the left side of its face, where one cheek is hugely swollen - puffed out like a balloon, shiny and red around one sore tusk - while big felt tears squirt from its squeezed-shut eyes."),
    ('std','pip',"stands small near the cave entrance in the foreground, looking up at the troll with cautious sympathy.")],
    extra="The troll is the one crying; Pip only watches from the entrance.",
    light="Dim cool cave light with a soft glow from the entrance."),
 'troll_panics': dict(refs=['pip','troll'], blocks=[
    ('std','troll',"scrambles up and away toward the back of the cave, arms flailing, mouth wide open in a terrified scream."),
    ('std','pip',"sprints toward the cave exit in the foreground, mouth also wide open in a scream, hat flapping.")],
    extra="Both are screaming; the troll flees toward the back of the cave while Pip flees toward the exit. Do not swap their directions.",
    light="Dim cave light, dust shaken loose from the ceiling."),
 'troll_toothpull': dict(refs=['pip','troll'], blocks=[
    ('std','troll',"sits leaning forward with its mouth stretched wide open, eyes crossed, its left cheek - on the viewer's right as the troll faces forward - still hugely swollen, shiny and red around the sore left tusk, gripping its own knees and holding very still."),
    ('std','pip',"digs their heels into the cave floor and leans far back, cheeks puffed with effort, hauling on a glowing rope of sparkling magic that stretches from the tip of their wand and loops around the sore tusk on the swollen side of the troll's mouth - the viewer's right.")],
    extra="Tiny Pip pulls; the huge troll holds still. The magic rope connects Pip's wand to the tooth. Do not swap their roles.",
    light="Warm golden glow from the magic rope in the dim cave."),
 'troll_gift': dict(refs=['pip','troll'], blocks=[
    ('std','troll',"sits smiling a wide, relieved smile with watery eyes, holding out the pulled fang - a single large curved white fang, as long as Pip's wand, with a rounded root - in its enormous fingers. Its smile shows one remaining fang on the viewer's left and a clear empty gap on the viewer's right where the sore fang used to be; no other teeth. Its left cheek is back to normal size."),
    ('std','pip',"stands in front of the troll, receiving the tooth in both flippers, proud and a little amazed.")],
    light="Warm soft cave light.",
    dev="Deliberate deviation: the troll is missing one tusk, freshly pulled, with a visible gap in its smile - otherwise it matches its reference."),
 'the_unicorn': dict(refs=['pip','unicorn'], blocks=[
    ('std','unicorn',"is tangled in the thorny vines, half-rearing with eyes wide, one leg caught, the vines pulled tight."),
    ('std','pip',"stands a few steps away, very still, one flipper raised gently, taking a slow calm breath.")],
    extra="The unicorn is the one tangled; Pip stands free. Do not swap their roles.",
    light="Muted afternoon light through the bare branches."),
 'unicorn_bolts': dict(refs=['pip','unicorn'], blocks=[
    ('std','unicorn',"leaps away through the thicket mid-bound, snapped vines trailing behind it like party ribbons."),
    ('std','pip',"stands alone by the empty brambles, lowering the wand with a thin wisp of smoke curling from its tip, face flat and unimpressed.")],
    light="Muted afternoon light, a few sparkles still fading in the air."),
 'unicorn_gift': dict(refs=['pip','unicorn'], blocks=[
    ('std','unicorn',"stands free and calm among the loosened vines, head bowed low to Pip, offering a single shimmering pale strand of mane."),
    ('std','pip',"cradles the shimmering strand in both flippers like a treasure, looking up at the unicorn.")],
    light="Soft golden light."),
 'core_tooth': dict(refs=['pip','branch'], blocks=[
    ('std','branch',"lies level across two flat stones in front of Pip."),
    ('std','pip',"kneels beside the branch with their glowing wand raised, guiding the troll's pulled fang - a large curved white fang with a rounded root - as it sinks halfway into the very middle of the wood inside a ring of warm golden spell-light.")],
    extra="Only Pip, the branch, and the sinking tooth - no troll in frame.",
    light="Warm golden spell-light in the dim cave.",
    dev="Deliberate deviation: a troll tooth is embedded halfway into the branch's middle, glowing - otherwise the branch matches its reference."),
 'core_mane': dict(refs=['pip','branch'], blocks=[
    ('std','branch',"lies level across two flat stones in front of Pip."),
    ('std','pip',"kneels beside the branch with their glowing wand raised, as a single long shimmering pale strand of unicorn mane winds itself around the middle of the branch in a glowing silver spiral, sinking into the bark.")],
    extra="Only Pip, the branch, and the glowing strand - no unicorn in frame.",
    light="Soft silver spell-light in the muted thicket.",
    dev="Deliberate deviation: a glowing silver strand spirals around the branch's middle - otherwise the branch matches its reference."),
 'the_waterfall': dict(refs=['pip','rival'], blocks=[
    ('std','rival',"stands near the pool soaked through, fur flattened and dripping, wringing water out of the hem of his red robe with both paws, scowling."),
    ('std','pip',"stands dry on a wet mossy boulder to the side, watching him.")],
    extra="Red Fox is the soaked, scowling one; Pip is dry and watching. Do not swap their roles.",
    light="Bright cool light with white mist drifting off the falls.",
    dev="Deliberate deviation: Red Fox's fur and robe are soaked flat and dripping - otherwise he matches his reference."),
 'the_bog': dict(refs=['pip'], blocks=[
    ('std','pip',"stands knee-deep in brown mud, robe hem soaked dark, batting at a little cloud of tiny felt insects around their head, face scrunched in disgust.")],
    light="Flat murky grey-green light."),
 'behind_the_falls': dict(refs=['pip'], blocks=[
    ('std','pip',"stands dripping at the mouth of the cavern with the glowing curtain of falling water behind them, facing the two passages - the left one glittering with crystal dust, the right one plain and dark.")],
    light="Cool blue light through the water curtain, with a faint sparkle from the glittering passage."),
 'collapsing_tunnel': dict(refs=['pip'], blocks=[
    ('std','pip',"sprints toward the viewer at full tilt, body leaning into the run mid-stride, one foot off the ground, mouth wide open in a yell, holding their hat on with one flipper."),
    ('raw',"Directly behind Pip the tunnel is caving in mid-collapse: large chunks of glittering fake quartz are falling and bouncing off the floor, cracks race across the ceiling, and a thick cloud of sparkling dust billows forward at Pip's heels.")],
    light="Dim tunnel light shot through with glinting dust from the collapse."),
 'mountain_falls': dict(refs=['pip'], blocks=[
    ('std','pip',"stands small on the winding trail in the lower foreground, back half-turned to the viewer, looking up at the distant mountain.")],
    extra="A wide establishing shot: the mist-wrapped mountain and its silver waterfall dominate the frame, and Pip is tiny on the trail below. No other characters.",
    light="Cool misty morning light, the sun catching the falling water."),
 'fox_brag': dict(refs=['rival'], blocks=[
    ('std','rival',"shown in close-up from the chest up on his rock ledge, chest puffed out, eyes closed in self-satisfaction, one paw flung out grandly mid-story. Above his head, filling the upper half of the frame, floats a large white felted thought-bubble cloud with little felt bubble-dots leading up from his head. Inside the bubble is his imagined scene: a small heroic version of Red Fox in a dramatic action pose hurling bright orange felt fireballs at a wall of blue ice, glittering chunks blasting away, his robe billowing like a cape.")],
    extra="A close-up composition: the real Red Fox occupies the lower part of the frame and the thought bubble fills most of the upper half. The fireball-throwing fox appears ONLY inside the felted thought bubble - it is an imagined scene. The real Red Fox holds no fire. No other characters anywhere in the image.",
    light="Soft layered glow from the crystals below, brighter warm light inside the bubble.",
    dev="Deliberate deviation: a felt thought bubble floats above Red Fox containing a miniature imaginary Red Fox - both versions of the fox match the fox reference."),
 'crystal_cavern': dict(refs=['pip','bait_crystal'], blocks=[
    ('std','pip',"stands small at the tunnel mouth at the edge of the cavern, head tilted all the way back, beak open in wonder, wand held loosely at their side."),
    ('std','bait_crystal',"dangles from the distant ceiling on a thin dark root, high above the center of the deep pit, turning slowly, small against the vastness.")],
    extra="A wide establishing shot: the cavern is huge and Pip is tiny at its edge, with the pit yawning in the middle of the floor. Red Fox does not appear in this image - no fox anywhere.",
    light="Soft layered glow from hundreds of crystals, deep shadow in the pit."),
 'focus_bound': dict(refs=['pip','branch','small_crystal'], blocks=[
    ('std','branch',"lies across a flat stone beside the foamy pool, polished smooth into a finished staff."),
    ('std','small_crystal',"hovers just above the staff's tip, sinking into a curl of pale wood that wraps around it like fingers closing, inside a ring of soft white spell-light."),
    ('std','pip',"kneels beside the stone with their wand raised, still damp from the pool, guiding the crystal gently into place with a look of quiet concentration.")],
    extra="Only Pip, the staff and the crystal - no other characters.",
    light="First golden dawn light over the pool mixing with the crystal's soft white glow.",
    dev="Deliberate deviation: the small crystal is being bound into the branch's tip and the wood curls around it - the branch is now a finished staff."),
 'the_crystal_chamber': dict(refs=['pip','rival','bait_crystal'], blocks=[
    ('std','bait_crystal',"dangles from the cavern ceiling on a thin dark root, directly over the deep pit."),
    ('std','rival',"perches comfortably on a high rock ledge above the deep pit, smirking down and pointing up at the dangling golden crystal."),
    ('std','pip',"stands at the chamber entrance below, small among the glowing crystals, looking up at the dangling crystal.")],
    extra="Red Fox is up on the ledge; Pip is down at the entrance. Do not swap their positions.",
    light="Soft glow from the crystals, deep shadow in the pit."),
 'into_the_pit': dict(refs=['pip','rival','bait_crystal'], blocks=[
    ('std','bait_crystal',"still dangles from its thin dark root high above the pit, far out of reach."),
    ('std','pip',"falls into the dark pit, flippers stretched up toward the dangling golden crystal above, hat lifting off their head."),
    ('std','rival',"leans over the pit edge high above, laughing hard.")],
    extra="Pip is the one falling; Red Fox only laughs from above. Do not swap their roles.",
    light="Crystal-glow from above fading into darkness below."),
 'the_choosing': dict(refs=['pip','big_crystal','small_crystal'], blocks=[
    ('std','big_crystal',"towers on the left side, blazing with light."),
    ('std','small_crystal',"rests on the chamber floor on the right side, glowing gently."),
    ('std','pip',"kneels between the two crystals, flippers hovering, looking from one to the other.")],
    extra="The huge crystal is on the left; the small crystal is on the right.",
    light="The big crystal's harsh glare meeting the small crystal's gentle glow."),
 'shattered': dict(refs=['pip','big_crystal'], blocks=[
    ('std','big_crystal',"bursts apart the moment Pip touches it, cracking into countless glittering shards that rain down over Pip."),
    ('std','pip',"recoils with flippers up, dismayed, sparkling dust settling on their hat and shoulders.")],
    light="One last bright flash from the shattering crystal.",
    dev="Deliberate deviation: the huge crystal is shown fracturing into shards mid-burst."),
 'crystal_chosen': dict(refs=['pip','small_crystal'], blocks=[
    ('std','pip',"shown in close-up from the chest up, holding the small crystal up in both flippers near their face, beaming a big warm smile, eyes bright, the crystal's glow lighting their face and the underside of their hat brim."),
    ('std','small_crystal',"rests in Pip's flippers, glowing with a perfectly steady, calm white light.")],
    extra="A close-up composition: Pip and the crystal fill the frame. No other characters anywhere in the image.",
    light="The crystal's soft steady white glow against the dim glittering cavern background.",
    dev="No deliberate deviations from the reference images."),
 'the_flood': dict(refs=['pip','rival','small_crystal'], blocks=[
    ('std','rival',"stands blocking the tunnel mouth with his arms crossed, smirking, while behind him a cracked wall of ice leaks streams of meltwater."),
    ('std','pip',"stands in the swirling meltwater in the foreground, clutching the small crystal tight to their chest, looking for a way out."),
    ('std','small_crystal',"is clutched against Pip's chest, glowing softly.")],
    extra="Red Fox blocks the tunnel; Pip stands out in the open chamber. Do not swap their positions.",
    light="Cold blue-green light reflecting off the rising water."),
 'cornered': dict(refs=['pip','rival','small_crystal'], blocks=[
    ('std','rival',"is braced sideways across the narrow tunnel with his legs pushed against the walls, arms crossed, chin just above the water, smirking."),
    ('std','pip',"is pressed close in the tight tunnel, water up to their chest, glaring, holding the small crystal up out of the water with one flipper."),
    ('std','small_crystal',"is held just above the waterline in Pip's flipper.")],
    extra="Red Fox is the one braced across the tunnel blocking the way; Pip is the one blocked. Do not swap their roles.",
    light="Dim tunnel light reflecting off dark rising water."),
 'swept_away': dict(refs=['pip','small_crystal'], blocks=[
    ('std','pip',"tumbles out of the base of the waterfall into the foamy pool, mid-splash with flippers empty."),
    ('std','small_crystal',"tumbles away separately through the foam, just out of reach.")],
    light="Bright churning white water."),
 'stuck_fast': dict(refs=['pip','momma_bird'], blocks=[
    ('raw',"Pip - A small round penguin wizard chick with black-and-white felted feathers, a little orange beak and orange feet, wearing a blue felt wizard robe and a tall floppy pointed blue wizard hat, both dotted with small yellow felt stars, matching the first reference image - is stuck fast INSIDE a narrow vertical crack in the tunnel wall: the crack's rock edges squeeze Pip's round belly at the widest point so the body bulges above and below the pinch, head and shoulders poking out one side, both orange feet dangling off the ground and kicking in the air, hat askew. Pip is emphatically NOT standing on the ground - the crack grips and holds the body mid-air."),
    ('std','momma_bird',"perches on a rock directly in front of Pip with her wings planted on her hips, glaring in silent, absolute fury.")],
    extra="The momma bird is not attacking - just staring.",
    light="Dim tunnel light."),
 'crystal_in_hand': dict(refs=['pip','rival','small_crystal'], blocks=[
    ('std','pip',"surfaces in the foamy pool, soaked and triumphant, holding the small crystal high overhead in one flipper."),
    ('std','small_crystal',"is held high in Pip's flipper, glowing."),
    ('std','rival',"is just visible through the curtain of falling water behind, small and blurry, sputtering in the flooded chamber with his hat drooping over one eye.")],
    extra="Pip is the triumphant one in the foreground pool; Red Fox is stuck behind the falls. Do not swap their roles.",
    light="Bright morning light catching the spray.",
    dev="Deliberate deviation: Red Fox is soaked, with his hat drooping - otherwise he matches his reference."),
 'home_again': dict(refs=['pip','teacher','branch','small_crystal'], blocks=[
    ('std','pip',"stands proudly in the middle of the study holding their finished wizard staff upright."),
    ('std','branch',"forms the body of the staff in Pip's flippers."),
    ('std','small_crystal',"is bound to the top of the staff, glowing softly."),
    ('std','teacher',"stands before Pip with wings clasped, eyes bright and proud.")],
    extra="Pip holds the staff; the teacher only watches, beaming.",
    light="Warm morning light through the tall pointed window.",
    dev="Deliberate deviation: the branch and the small crystal are assembled together into one finished staff."),
}

COVER = dict(refs=['pip','branch','small_crystal'], loc='forest_path', blocks=[
    ('std','pip',"stands in the middle of the path facing the viewer with a brave, excited smile, holding their finished wizard staff upright beside them."),
    ('std','branch',"forms the body of the staff."),
    ('std','small_crystal',"is bound to the top of the staff, glowing softly.")],
    extra="A wide storybook-cover composition with Pip centered. No text or lettering anywhere in the image.",
    light="Warm golden adventure light along the path.",
    dev="Deliberate deviation: the branch and the small crystal are assembled together into one finished staff.")

def assemble(spec, loc_desc):
    refs = spec['refs']
    parts = [ART, loc_desc]
    order = ", ".join(f"{ORDINALS[i]} {NAMES[r]}" for i, r in enumerate(refs))
    parts.append(f"Reference images are provided in this order: {order}.")
    for b in spec['blocks']:
        if b[0] == 'raw':
            parts.append(b[1])
        else:
            _, rid, action = b
            idx = refs.index(rid)
            name = NAMES[rid]
            name_cap = name[0].upper() + name[1:] if not name[0].isupper() else name
            parts.append(f"{name_cap}, matching the {ORDINALS[idx]} reference image - {ALLDESC[rid]} - {action}")
    if spec.get('extra'):
        parts.append(spec['extra'])
    parts.append(spec['light'])
    parts.append(spec.get('dev', "No deliberate deviations from the reference images."))
    return " ".join(parts)

# ---------------- apply to story JSON ----------------
assert set(S) == set(d['scenes']), (set(S) ^ set(d['scenes']))
refdir_runtime = f"data/stories/{SLUG}/_refs"
d['characters'] = {k: {"description": v, "referenceImage": f"{refdir_runtime}/{k}.png"} for k, v in CHARACTERS.items()}
d['items'] = {k: {"description": v, "referenceImage": f"{refdir_runtime}/{k}.png"} for k, v in ITEMS.items()}
# keep top-level key order similar to stormy: slug,title,artStyle,startScene,characters,items,locations,scenes
d = {k: d[k] for k in ['slug','title','artStyle','startScene','characters','items','locations','scenes']}

manifest = {'refs': [], 'scenes': []}
refdir_abs = f"{ROOT}/game/data/stories/{SLUG}/_refs"

# Item descriptions reference Pip for scale, which pulls stray characters into
# reference renders - use character-free wording for the ref prompts only.
REF_DESC = dict(ALLDESC)
REF_DESC['big_crystal'] = "A huge dazzling pale-pink felted crystal with sharp bright facets, blazing with light from within."
REF_DESC['small_crystal'] = "A single small clear felted crystal, smooth and simple, glowing with a soft steady white light."
REF_DESC['branch'] = "A strong straight living branch of pale felted wood with a few small green felt leaves near its tip, propped upright."
REF_DESC['bait_crystal'] = "A dazzling honey-gold teardrop-shaped felted crystal with many sharp sparkling facets, glowing warmly from within."

# For item refs, the artStyle preamble's "diorama, miniature scene" wording invites
# invented scenery/characters - use a product-shot style line instead.
ITEM_STYLE = ("A single needle-felted wool object photographed like a handmade craft product shot, "
              "with visible needle-felting texture and wispy loose wool fibers, an earthy muted color "
              "palette, warm soft lighting, on a plain empty warm grey felt backdrop.")

for rid in REF_ORDER:
    if rid in ITEMS:
        prompt = (f"{ITEM_STYLE} The object: {REF_DESC[rid]} It sits alone, centered, the whole object "
                  f"clearly visible. The frame contains nothing except this one object and the plain "
                  f"backdrop - no people, no animals, no characters, no buildings, no base, no ground, "
                  f"no props, no scenery, no text.")
    else:
        prompt = (f"{ART} {REF_DESC[rid]} Shown alone, centered, on a plain warm grey felt backdrop, "
                  f"full body from head to feet clearly visible. The image contains only this character "
                  f"and nothing else - no people, no animals, no other characters, no props, no scenery, no text.")
    pfile = f"{PROMPTS}/ref_{rid}.txt"
    open(pfile, 'w').write(prompt)
    manifest['refs'].append({'id': rid, 'prompt': pfile, 'out': f"{refdir_abs}/{rid}.png", 'refs': []})

for sid, s in d['scenes'].items():
    spec = S[sid]
    if sid in TEXT: s['text'] = TEXT[sid]
    if sid in CHOICES: s['choices'] = [{'text': t, 'target': g} for t, g in CHOICES[sid]]
    if sid in IMG_DESC: s['imageDescription'] = IMG_DESC[sid]
    s['LLMImageDescription'] = assemble(spec, LOC[s['location']]['description'])
    # Point at the .webp once optimize-images has produced it; .png only pre-optimization.
    png_rel, webp_rel = (f"data/stories/{SLUG}/{sid}.{ext}" for ext in ('png', 'webp'))
    if os.path.exists(f"{ROOT}/game/{png_rel}") or not os.path.exists(f"{ROOT}/game/{webp_rel}"):
        s['image'] = png_rel
    else:
        s['image'] = webp_rel
    pfile = f"{PROMPTS}/{sid}.txt"
    open(pfile, 'w').write(s['LLMImageDescription'])
    manifest['scenes'].append({'id': sid, 'prompt': pfile,
        'out': f"{ROOT}/game/data/stories/{SLUG}/{sid}.png",
        'refs': [f"{refdir_abs}/{r}.png" for r in spec['refs']]})

cover_desc = assemble(COVER, LOC[COVER['loc']]['description'])
pfile = f"{PROMPTS}/cover.txt"
open(pfile, 'w').write(cover_desc)
manifest['scenes'].append({'id': 'cover', 'prompt': pfile,
    'out': f"{ROOT}/game/data/stories/{SLUG}/cover.png",
    'refs': [f"{refdir_abs}/{r}.png" for r in COVER['refs']]})

json.dump(d, open(STORY, 'w'), indent=2, ensure_ascii=False)
json.dump(manifest, open(f"{OUTDIR}/pip_manifest.json", 'w'), indent=1)
print(f"OK: {len(manifest['refs'])} refs, {len(manifest['scenes'])} scene/cover images")
print("Sample LLM desc (the_grove):\n", d['scenes']['the_grove']['LLMImageDescription'][:400])
