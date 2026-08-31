# -*- coding: utf-8 -*-
"""Corrections for the 2026-08-29 closing-night recordings.

Only mishearings are corrected: things the speaker said that the model wrote down
wrongly. Things the speaker got wrong himself are left alone and listed in
FACTUAL_NOTES so they can be flagged rather than silently rewritten.
"""
import re

CORRECTIONS = [
    # --- spacing and punctuation artefacts ---
    (r"(\d) ,(\d)", r"\1,\2"),
    (r"(\w) -(\w)", r"\1-\2"),
    (r"\s+([,.?!])", r"\1"),

    # --- British spellings ---
    (r"\blabor\b", "labour"),
    (r"\bemotional labor\b", "emotional labour"),
    (r"\brealize\b", "realise"),
    (r"\brealized\b", "realised"),
    (r"\brealizing\b", "realising"),
    (r"\brecognize\b", "recognise"),
    (r"\brealization\b", "realisation"),
    (r"\borganize", "organise"),
    (r"\bapologize\b", "apologise"),
    (r"\bdefense lawyer", "defence lawyer"),
    (r"\bfavorite\b", "favourite"),

    # --- names of people ---
    (r"\bRichard Toy\b", "Richard Toye"),
    (r"\bJohn Paul Sartre\b", "Jean-Paul Sartre"),
    (r"\bA(?:li|leigh|rleigh) Russell Hock ?[sc]hield\b", "Arlie Russell Hochschild"),
    (r"\bAli Russell\b", "Arlie Russell"),
    (r"\bHuntress Thompson\b", "Hunter S. Thompson"),
    (r"\bCorey Doctor-Roe\b", "Cory Doctorow"),
    (r"\bCorey Doctor\b", "Cory Doctorow"),
    (r"\bColumn Tobin\b", "Colm Toibin"),
    (r"\bJohn Mill said\b", "John Mills said"),
    (r"\bAnne Lamott\b", "Anne Lamott"),

    # --- names of places, publishers, products ---
    (r"\bA[- ]?[Pp]ress\b", "Apress"),
    (r"\bGramerle\b", "Grammarly"),
    (r"\bGerton College\b", "Girton College"),
    (r"\bin Oldgate\b", "at Aldgate"),
    (r"\bOldgate\b", "Aldgate"),
    (r"\blimehouse\b", "Limehouse"),
    (r"\bthe meadows\b", "the Meadows"),
    (r"\bEdinburgh Town Centre\b", "Edinburgh town centre"),
    (r"\bAndaman Islands\b", "Andaman Islands"),

    # --- titles ---
    (r"\bdelivering the impossible\b", "Delivering the Impossible"),
    (r"\byou can write a book\b", "You Can Write a Book"),
    (r"\bthe language wars\b", "The Language Wars"),
    (r"\bHow to Read a Book\b", "How to Read a Book"),
    (r"\bhow to read a book\b", "How to Read a Book"),
    (r"\bwar and peace\b", "War and Peace"),
    (r"\bThe Biscuit Tin and the Biscuit\b", "The Biscuit Tin and the Biscuit"),
    (r"\bchapter ship\b", "Chapter Ship"),
    (r"\bScott of the Antarctic\b", "Scott of the Antarctic"),
    (r"\bMuffrey's Law\b", "Muphry's Law"),
    (r"\bBird by Bird\b", "Bird by Bird"),
    (r"\bThe Managed Heart\b", "The Managed Heart"),
    (r"\bRomanticy\b", "romantasy"),

    # --- show vocabulary ---
    (r"\bhaving salt for six years\b", "having sulked for six years"),
    (r"\bI salt for six years\b", "I sulked for six years"),
    (r"\bI sought for six years\b", "I sulked for six years"),
    (r"\bscarier commits\b", "scarier commutes"),
    (r"\bhalf ?-?assed\b", "half-arsed"),
    (r"\btenth of an ass\b", "tenth of an arse"),
    (r"\btenth, 10th arse\b", "tenth of an arse"),
    (r"\bsixth of an arse\b", "sixth of an arse"),
    (r"\bwhole ass\b", "whole arse"),
    (r"\bSeen, not genius\b", "Scene, not genius"),
    (r"\bseen not genius\b", "scene, not genius"),
    (r"\bThe scene not genius thing\b", "The scene, not genius thing"),
    (r"\bstuckedness\b", "stuckness"),

    # --- misheard phrases ---
    (r"\bin a matter of fat way\b", "in a matter-of-fact way"),
    (r"\bnarrow and three quarters\b", "an hour and three quarters"),
    (r"\bpaddle around in the shall end\b", "paddle around in the shallow end"),
    (r"\bdoing the swim in\b", "doing the swimming"),
    (r"\byou can talk your way out or something\b", "you can talk your way out of something"),
    (r"\bnot that bigger victory\b", "not that big a victory"),
    (r"\ba bit of weird thing\b", "a bit of a weird thing"),
    (r"\bcan I get the cover change\b", "can I get the cover changed"),
    (r"\bif you want to get the code change\b", "if you want to get the cover changed"),
    (r"\bI know other shows I've had nobody\b", "I know other shows have had nobody"),
    (r"\bI'm not saying you shouldn't be playing\b", "I'm not saying you shouldn't be playing"),
    (r"\bwe can't hang out with us guys\b", "we can't hang out with those guys"),
    (r"\bthey're feeling one motion\b", "they're feeling one emotion"),
    (r"\bI got no people for a show\b", "I got no people in for a show"),
    (r"\beither a beer or some fishing chips\b", "either a beer or some fish and chips"),
    (r"\beither a beer or some fish drinks\b", "either a beer or some fish and chips"),
    (r"\bI've done at 12 at show run\b", "I've done a twelve date show run"),
    (r"\bthe theatre gods way and the theatre is for gods\b",
     "the theatre gods' way, and the theatre is for gods"),
    (r"\bso that they're a better way\b", "so that they're better"),
    (r"\bI'm not in the business of dealing the shit\b",
     "I'm not in the business of dealing in shit"),
    (r"\bthe idea of there been a pirate ship\b", "the idea of there being a pirate ship"),
    (r"\bthe old subconscious, is trying to tell me\b",
     "the old subconscious trying to tell me"),
    (r"\bmore quickly is it quicker or more quickly\b",
     "more quickly. Is it quicker, or more quickly?"),
    (r"\bwhat card have we got next\b", "what card have we got next"),
    (r"\bshouldn't interrupt your flow of stringer\b",
     "shouldn't interrupt your flow, Stringer"),
    (r"\bBe careful on my glasses\b", "Careful of my glasses"),
    (r"\bit's one of the blues men\b", "it's one of the blues men"),
    (r"\bwas it muddy waters\b", "was it Muddy Waters"),
    (r"\bwas it BB King\b", "was it B.B. King"),
    (r"\bstart to mix a martini and somebody will jump out\b",
     "start to mix a martini and somebody will jump out"),
    (r"\bwith the whole odyssey thing\b", "with the whole Odyssey thing"),
    (r"\bin old and old and olden times\b", "in olden times"),

    # --- Whisper repetition artefacts ---
    (r"(?:\bum,?\s*){4,}", "um, "),
    (r"(?:\buh,?\s*){4,}", "uh, "),
    (r"\ba bunch, a bunch of emotions\b", "a bunch of emotions"),
    (r"\bstaying in the pool, staying in the pool\b", "staying in the pool, staying in the pool"),


    # --- second pass: caught on review of the first corrected transcript ---
    (r"\bthey weren't half ass\b", "they weren't half-arsed"),
    (r"\bhalf ass\b", "half-arsed"),
    (r"\bin the shall\.? end\b", "in the shallow end"),
    (r"\bthe whole kind of 10th, 10th arse\b", "the whole tenth of an arse thing"),
    (r"\b10th, 10th arse\b", "tenth of an arse"),
    (r"[Yy]ou [Cc]an [Ww]rite a book\b", "You Can Write a Book"),
    (r"\bwriting is a bit like he also switched\b", "writing is a bit like swimming, because he also swims"),
    (r"\bthere may have been better times there, but\b", "there may have been better times, but"),
    (r"\bwas a lot of the work that I to do\b", "was a lot of the work that I had to do"),
    (r"\bI'm still not got quite the right word\b", "I've still not got quite the right word"),
    (r"\bMinotaur's and AI\b", "Minotaurs and AI"),
    (r"\bgrammar for people who aren't twats\b", "Grammar For People Who Aren't Twats"),
    (r"\bthe idea of a shitty first draft\b", "the idea of a shitty first draft"),
    (r"\bit's a narrow and three quarters\b", "it was an hour and three quarters"),
    (r"\bwhich was it was it was\b", "which was"),
    (r"\bwhat I was talking about\?", "what was I talking about?"),
    (r"\bYes, what I was talking about\b", "Yes, what was I talking about"),
    (r"\bhave to edit this bit out\b", "have to edit this bit out"),
    (r"\bjust a minute, just a kind of little yes, just a little practice\b",
     "just a minute, just a little... yes, just a little practice"),
    (r"\bI had a straightforward way of doing this show\b",
     "I had a straightforward way of doing this show"),

    (r"\bif you are interesting writing a book\b", "if you are interested in writing a book"),
    (r"\bso if you are interesting writing\b", "so if you are interested in writing"),

    # --- tidy up ---
    (r"\s{2,}", " "),
]

# Things Mark says that are wrong, left in the transcript as spoken.
FACTUAL_NOTES = [
    'At 09:41 the Bird by Bird story is attributed to "a chap called Edward Audubon" and '
    '"The Birds of North America". Anne Lamott tells it about her father and her brother; '
    'the bird book is The Birds of America by John James Audubon.',
    'At 15:58 How to Read a Book is dated "late 30s early 40s". It was published in 1940 '
    'by Mortimer Adler, so the range is right but the author is not named.',
    'At 45:18 the Cory Doctorow title is not recalled ("something about Minotaurs and AI"). '
    'He says on tape that he cannot remember it.',
]


def fix(text):
    for pat, rep in CORRECTIONS:
        text = re.sub(pat, rep, text)
    return text.strip()


def fix_segments(segs):
    """Correct a list of {s,e,t} segments at document level, then put the words
    back onto the original segment boundaries so the timings still line up."""
    import difflib
    words, bounds = [], [0]
    for seg in segs:
        words += seg["t"].split()
        bounds.append(len(words))
    new_words = fix(" ".join(words)).split()

    sm = difflib.SequenceMatcher(a=words, b=new_words, autojunk=False)
    mapping = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        for i in range(i1, i2 + 1):
            if i not in mapping:
                span = max(i2 - i1, 1)
                mapping[i] = min(len(new_words),
                                 j1 + int(round((i - i1) / span * (j2 - j1))))
    mapping[len(words)] = len(new_words)
    nb = [mapping.get(b, b) for b in bounds]
    for i in range(1, len(nb)):
        if nb[i] < nb[i-1]:
            nb[i] = nb[i-1]
    nb[-1] = len(new_words)

    out = []
    for k, seg in enumerate(segs):
        text = " ".join(new_words[nb[k]:nb[k+1]]).strip()
        if text:
            out.append({"s": seg["s"], "e": seg["e"], "t": text})
    return out
