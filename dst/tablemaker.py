"""
this script is to make a table of character interactions in dst speech files
so that you can easily see what one character says about another.
it has a few other categories too, to see when a character mentions some other topic.

flaws in this script:

it's hard to tell what the described thing is sometimes.
a fix would be to use the strings file to lookup the name of the thing,
and change pattern detection so it's not so line-by-line.
this would avoid confusing prefab names  (HALLOWEENCANDY_11),
and ambiguous sub-keys (GENERIC, BURNT)

the gui could be better.
maybe make the table scale better and make the borders prettier.
maybe use clicking so you don't accidentally deselect a cell while trying to scroll
"""
import re
import html

#this address should point to the scripts folder in the scripts databundle
#but the scripts databundle is a zip file, so you'll have to extract it.
address = r"C:\Program Files (x86)\Steam\SteamApps\common\Don't Starve Together Beta\data\databundles\scripts" + "\\"

speeches = [
    "wathgrithr",
    "waxwell",
    "webber",
    "wendy",
    "wickerbottom",
    "willow",
    "wilson",
    "wolfgang",
    "woodie",
    "wx78",
    "winona",
    "wortox"
]
specifics = {
    "wathgrithr": [
        "wathgrithr",
        "wathgrithrhat",
        "spear_wathgrithr"
    ],
    "waxwell": [
        "waxwell",
        "waxwelljournal",
        "chesspiece_formal",
        "statuemaxwell",
        "maxwell",
        "maxwellhead",
        "shadowdigger"
    ],
    "webber": [
        "webber",
        "webberskull",
        "webber_spider_minion"
    ],
    "wendy": [
        "wendy",
        "abigail",
        "abigailheart",
        "abigail_flower"
    ],
    "wickerbottom": [
        "wickerbottom",
        "book_birds",
        "book_tentacles",
        "book_gardening",
        "book_sleep",
        "book_brimstone",
        "book_fossil"
    ],
    "willow": [
        "willow",
        "lighter",
        "bernie_active",
        "bernie_inactive",
        "lavaarena_bernie"
    ],
    "wilson": [
        "wilson",
        "chesspiece_pawn",
        "resurrectionstatue"
    ],
    "wolfgang": [
        "wolfgang",
        ],
    "woodie": [
        "woodie",
        "lucy",
        "lavaarena_lucy"
    ],
    "wx78": [
        "wx78",
        "trinket_11" #lying robot
    ],
    "wes": [
        "wes",
        "balloon",
        "balloons_empty"
    ],
    "charlie": [
        "rose",
        "chesspiece_muse",
        "multiplayer_portal",
        "statue_marble",
        "stagehand",
        "announce_charlie",
        "announce_charlie_attack",
        "shadowheart"
    ],
    "misc": [
        "trinket_10",
        "player",
        "maxwelllight",
        "maxwelllock",
        "maxwellthrone"
    ],
    "family": [
        ],
    "laughter": [
        ],
    "atriumstuff": [
        "shadowheart",
        "atrium_rubble",
        "atrium_statue",
        "atrium_light",
        "atrium_gate",
        "atrium_key",
        "cantshadowrevive",
        "fossil_piece",
        "stalker",
        "stalker_atrium",
        "stalker_minion",
        "thurible",
        "atrium_overgrowth",
        "shadowchanneler",
        "announce_atrium_destabilizing",
        "announce_ruins_reset",
        "armorskeleton"
    ],
    "winona": [
        "winona",
        "sewing_tape",
        "winona_catapult",
        "winona_spotlight",
        "winona_battery_low",
        "winona_battery_high"
    ],
    "forge": [
        "lavaarena_portal",
        "lavaarena_keyhole",
        "lavaarena_keyhole_full",
        "lavaarena_battlestandard",
        "lavaarena_spawner",
        "healingstaff",
        "fireballstaff",
        "hammer_mjolnir",
        "spear_gungnir",
        "blowdart_lava",
        "blowdart_lava2",
        "lavaarena_armorlight",
        "lavaarena_armorlightspeed",
        "lavaarena_armormedium",
        "lavaarena_armormediumrecharger",
        "lavaarena_armorheavy",
        "lavaarena_armorextraheavy",
        "lavaarena_feathercrownhat",
        "lavaarena_healingflowerhat",
        "lavaarena_lightdamagerhat",
        "lavaarena_strongdamagerhat",
        "lavaarena_tiaraflowerpetalshat",
        "lavaarena_eyecirclehat",
        "lavaarena_rechargerhat",
        "lavaarena_healinggarlandhat",
        "lavaarena_crowndamagerhat",
        "lavaarena_boarlord",
        "boarrior",
        "boaron",
        "trails",
        "turtillus",
        "snapper",
        "announce_reviving_corpse",
        "announce_revived_other_corpse",
        "announce_revived_from_corpse",
        "lavaarena_lucy",
        "webber_spider_minion",
        "book_fossil",
        "lavaarena_bernie"
    ],
    "wortox": [
        "wortox"
    ],
    "lunar": [
        "BOATFRAGMENT01",
        "BOATFRAGMENT02",
        "BOATFRAGMENT03",
        "BOATFRAGMENT04",
        "BOATFRAGMENT05",
        "BOAT_LEAK",
        "MAST",
        "SEASTACK",
        "FISHINGNET",
        "ANTCHOVIES",
        "STEERINGWHEEL",
        "ANCHOR",
        "BOATPATCH",
        "BURNING",
        "BURNT",
        "CHOPPED",
        "GENERIC",
        "DRIFTWOOD_LOG",
        "BURNING",
        "BURNT",
        "CHOPPED",
        "GENERIC",
        "GENERIC",
        "HELD",
        "MOONBUTTERFLYWINGS",
        "MOONBUTTERFLY_SAPLING",
        "ROCK_AVOCADO_FRUIT",
        "ROCK_AVOCADO_FRUIT_RIPE",
        "ROCK_AVOCADO_FRUIT_RIPE_COOKED",
        "ROCK_AVOCADO_FRUIT_SPROUT",
        "BARREN",
        "WITHERED",
        "GENERIC",
        "PICKED",
        "DISEASED",
        "DISEASING",
        "BURNING",
        "DEAD_SEA_BONES",
        "GENERIC",
        "BOMBED",
        "GLASS",
        "MOONGLASS",
        "MOONGLASS_ROCK",
        "BATHBOMB",
        "GENERIC",
        "CLOSED",
        "DUG_TRAP_STARFISH",
        "GENERIC",
        "SLEEPING",
        "DEAD",
        "MOONSPIDERDEN",
        "GENERIC",
        "RIPE",
        "SLEEPING",
        "GENERIC",
        "HELD",
        "SLEEPING",
        "MOONGLASSAXE",
        "GLASSCUTTER",
        "GENERIC",
        "MELTED",
        "ICEBERG_MELTED",
        "MINIFLARE",
        "GENERIC",
        "NOLIGHT",
        "MOON_ALTAR_WIP",
        "GENERIC",
        "MOON_ALTAR_IDOL",
        "MOON_ALTAR_GLASS",
        "MOON_ALTAR_SEED",
        "MOON_ALTAR_ROCK_IDOL",
        "MOON_ALTAR_ROCK_GLASS",
        "MOON_ALTAR_ROCK_SEED",
        "GENERIC",
        "BURNT",
        "SEAFARER_KIT",
        "BOAT_ITEM",
        "STEERINGWHEEL_ITEM",
        "ANCHOR_ITEM",
        "DEAD",
        "GENERIC",
        "SLEEPING",
        "DEAD",
        "GENERIC",
        "SLEEPING",
        "DEAD",
        "GENERIC",
        "HELD",
        "SLEEPING",
        "GESTALT",
        "GENERIC",
        "PICKED",
        "BULLKELP_ROOT",
        "KELPHAT",
        "KELP",
        "KELP_COOKED",
        "KELP_DRIED",
        "WALKINGPLANK"
    ]
}

aliases = {
    "wathgrithr": [
        "wigfrid",
        "viking"
    ],
    "waxwell": [
        "maxwell",
        "magician",
        "frail human"
    ],
    "webber": [
        "webber",
        "spider child",
        "monster child"
    ],
    "wendy": [
        "wendy",
        "abigail",
        "abby"
    ],
    "wickerbottom": [
        "librarian",
        "wicker",
        "brainlady"
    ],
    "willow": [
        "willow"
    ],
    "wilson": [
        "wilson"
    ],
    "wolfgang": [
        "wolfgang",
        "strongman"
    ],
    "woodie": [
        "woodie",
        "lucy",
        "lumberjack",
        "beaver",
    ],
    "wx78": [
        "wx"
    ],
    "wes": [
        "\\bwes\\b"
    ],
    "charlie": [
        "rose",
        "charlie"
    ],
    "misc": [
    ],
    "family": [
        "mother",
        "father",
        "\\bparent\\b",
        "grandparent",
        "grandpa",
        "grandma",
        "grandchild",
        "in-law",
        "wife",
        "husband",
        "spouse",
        "\\buncle\\b",
        "\\baunt\\b",
        "cousin",
        "nephew",
        "\\bniece",
        "granddad",
        "\\bdad\\b",
        "mom\\b",
        "ancestor",
        "sibling",
        "sister",
        "brother",
        "\\bson\\b",
        "grandson",
        "daughter\\b"
    ],
    "laughter": [
        "\\ba?(?:ha)+h?\\b",
        "\\blaugh",
        "heehee",
        "hee hee",
        "ho ho",
        "hehe"
    ],
    "atriumstuff": [
        ],
    "winona": [
        "winona"
    ],
    "forge": [
    ],
    "wortox": [
    ],
    "lunar": [
    ]
}
specialcases = {
    "wathgrithr": {},
    "waxwell": {
        "charlie": [
            "WINTER_FOOD9"
        ]
    },
    "webber": {},
    "wendy": {},
    "wickerbottom": {},
    "willow": {},
    "wilson": {},
    "wolfgang": {
        "woodie": [
            "TRINKET_14"
        ]
    },
    "woodie": {},
    "wx78": {},
    "winona": {},
    "wortox": {}
}
def mastermaker():
    dump = open("master.txt", "a")
    master = {}
    for k in speeches:
        master[k] = {}
    
    for k in sorted(master):
        for s in sorted(specifics):
            master[k][s] = []
    
    #ugh why did i parse this like this....
    #in my defence, i have to catch some lua comments,
    #so i can't just read this as a dict.
    #still, though, this looks kind of ugly.
    #it's from 2016, so you can't judge me too much.
    
    for char in sorted(master):
        print(char)
        speech = open(address + "speech_" + char + ".lua", "r").read()
        for described in master[char]:
            if described in specialcases[char]:
                specials = specialcases[char][described]
            else:
                specials = []
            for alias in specifics[described] + specials:
                match = re.search( r"\s+" + alias + r" =.*,.*", speech, re.I)
                if match == None: #for bracket stuff
                    match = re.search( r"\s+" + alias + r" =[^}]*},", speech, re.I|re.M)
                if match:
                    master[char][described].append(match.group())
            for alias in aliases[described]:
                match = re.findall( r"^\s+.*\".*" + alias + r".*\",.*$", speech, re.I|re.M)
                for quote in match:
                    if not quote in master[char][described]:
                        master[char][described].append(quote)
            if char == described: #for inspectself
                match = re.search( r"\s+" + "inspectself" + r" =.*,.*", speech, re.I|re.M)
                if match:
                    if not match.group() in master[char]["charlie"]:
                        master[char][described].append(match.group())

        
        
        if char == "waxwell": #charle comments
            match = re.findall( r"^\s+.*--.*\.\.\..*$", speech, re.I|re.M)
            #they end in ellipses
            for quote in match:
                if not quote in master[char]["charlie"]:
                    master[char]["charlie"].append(quote)
        
                
    
    return master

def masterhandler(first,second):
    for i in m[first][second]:
        print(i)
mh = masterhandler

def htmltablemaker():
    dump = open("table.html", "w")

    dump.write("""<style>
td .hideifintable {display:none;}
table {
  overflow: hidden;
}

td, th {
  padding: 1px;
  position: relative;
  outline: 0;
}

body:not(.nohover) tbody tr:hover {
  background-color: #ffa;
}

td:hover::after,
thead th:not(:empty):hover::after,
td:focus::after,
thead th:not(:empty):focus::after { 
  content: '';  
  height: 10000px;
  left: 0;
  position: absolute;  
  top: -5000px;
  width: 100%;
  z-index: -1;
}

td:hover::after,
th:hover::after {
  background-color: #ffa;
}

td:focus::after,
th:focus::after {
  background-color: lightblue;
}
</style>""")
    dump.write("<table border=\"1\">\n")
    dump.write("<tr>\n")
    dump.write("<td/>")
    for described in sorted(m["wilson"]):
        dump.write("<td>"+described+"</td>")
    dump.write("</tr>")
    for speaker in sorted(m):
        dump.write("<tr>")
        dump.write("<td>"+speaker+"</td>\n")
        for described in sorted(m[speaker]):
            dump.write("<td id=\""+speaker+described+"\" class=\""+speaker+" "+described+"\" onmouseover=\"document.getElementById('changer').innerHTML = document.getElementById('"+speaker+described+"').innerHTML;\"><div class=\"hideifintable\" ") #good luck
            dump.write("<ul><pre>")
            for i in m[speaker][described]:
                dump.write("<li>"+html.escape(i)+"</li>")
            dump.write("</pre></ul>")
            dump.write("</div></td>\n")
        dump.write("</tr>")
    dump.write("</table><div id=\"changer\">mouse over cells to display quotes. the speaker is on the left, the subject is on the top.</div>")

    dump.close()

m = mastermaker()
htmltablemaker()
