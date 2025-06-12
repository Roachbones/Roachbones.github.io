/*
    “Story files produced by Inform tend not to contain elaborate typographical effects. They would only distract. Like a novel, a classic work of IF is best presented in an elegant but unobtrusive font.”
            —The Inform Recipe Book, §12.1. Typography

anpa ma is not a classic work of IF. In this file we implement elaborate typographical effects. */

window.currentOrthography = "alphabetic";

const UPHILL_INCANTATION = "sina tawa sewi li tawa sewi li tawa sewi";
const DESCENT_INCANTATION = "sina tawa anpa li tawa anpa li tawa anpa";

window.twitchingWords = []

function twitch() {
    let twitchChance = 0.055;
    if (window.twitchingWords.length > 7) {
        // don't go so wild with the twitching for long dialogue
        twitchChance = 0.015;
    }
    window.twitchingWords.forEach(word => {
        if (Math.random() < twitchChance) {
            const x = (Math.random() - 0.5) * 2;
            const y = (Math.random() - 0.5) * 2;
            word.style.setProperty('--tx', `${x}px`);
            word.style.setProperty('--ty', `${y}px`);
        } else {
            word.style.setProperty('--tx', '0px');
            word.style.setProperty('--ty', '0px');
        }
    });
    window.twitchyTimeoutId = setTimeout(twitch, 35);
}


document.addEventListener("DOMContentLoaded", function(_event){
	window.bufferWindow = document.querySelector('.BufferWindow');
	window.gridLine = document.querySelector('.GridLine');
	
	updateStatusLine = function (statusLine) {
	    console.log(statusLine);
	    
	    if (statusLine.match(/n Lasina\s*$/)) {
            currentOrthography = "alphabetic";
			windowport.classList.add("alphabetic");
			windowport.classList.remove("logographic");
        }
        else if (statusLine.match(/elen.pona\s*$/)) {
            currentOrthography = "logographic";
			windowport.classList.add("logographic");
			windowport.classList.remove("alphabetic");
        }
	    
	    [leftHandStatusLine, rightHandStatusLine] = statusLine.trim().split(/\s\s+/);
	    rightHandStatusLine = rightHandStatusLine || "";
        leftSpan = document.createElement("span");       rightSpan = document.createElement("span");
        leftSpan.innerText = leftHandStatusLine;         rightSpan.innerText = rightHandStatusLine;
        leftSpan.classList.add("left-hand-status-line"); rightSpan.classList.add("right-hand-status-line");
        window.gridLine.replaceChildren(leftSpan, document.createTextNode(" "), rightSpan);
	}
	
	updateStatusLine(gridLine.textContent);
	
	gridLine.originalAppendChild = gridLine.appendChild
	    gridLine.appendChild = function(e) {
	        statusLine = e.textContent;
	        if (statusLine.includes("    ")) {
	            updateStatusLine(statusLine);
	        } else {
	            console.log("tiny status line moment");
	            this.originalAppendChild(e);
	        }
	}
	
	// may need to add more here depending on how well resuming works
	for (bufferLine of bufferWindow.children) {
	    bufferLine.classList.add(currentOrthography);
	}
	
	bufferWindow.originalAppendChild = bufferWindow.appendChild
	bufferWindow.appendChild = function(bufferLine) {
	    bufferLine.originalAppendChild = bufferLine.appendChild
	    bufferLine.classList.add(currentOrthography);
	    bufferLine.appendChild = function(f) {
            if (f.innerText.trim().endsWith("❧")) {
                f.classList.add("hedera");
            }
            
            /* Two spaces after a period looks a little better in nasin nanpa,
               but doing that programmatically in Inform would be a pain. */
            if (currentOrthography == "logographic" && f.children.length == 0) {
                f.textContent = f.textContent.replaceAll(/[.?!] \b/g, '$& ');
            }
            
            if (currentOrthography == "logographic" && f.innerText.startsWith("(") && f.innerText.endsWith(")")) {
                /* Probably a parenthesized parser disclaimer for implicitly choosing an object.
                   These are caused by this line of code in the i6 parser:
                     print "("; PrintCommand(from); print ")^";
                   This looks bad in nasin nanpa since it uses parens for ligatures.
                   This would be a pain to modify in Inform, so let's just bodge it here for now. */
                f.innerText = f.innerText.slice(1, -1);
                f.classList.add("parser-guess");
            }
            
		    /* Climbing uphill */
		    if (f.textContent.startsWith(UPHILL_INCANTATION)) {
			    this.classList.add("uphill");
		    }
		    if (f.textContent.startsWith(DESCENT_INCANTATION)) {
			    this.classList.add("descent");
		    }
		    if (f.classList.contains("InvisibleCursor")) {
	            return bufferLine.originalAppendChild(f);
	        }
		    if (this.classList.contains("descent")) {
		        // This is probably a "li tawa anpa" thing. Break it up.
		        prose = f.textContent;
		        while (prose.includes(" l")) {
		            prose = prose.replace(" l"," <span class=v>l");
		            prose = prose + "</span>";
		        }
		        f.innerHTML = prose;
		        f.classList.add("v");
		        // Instead of appending this span to the bufferLine,
		        // we actually want to append it to its child, or its child's child if it exists, and so on.
		        // This nestedness permits a sort of neat typographic pirouette via rotation css,
		        // used for narrating descent.
		        if (this.children.length == 0) {
		            return this.originalAppendChild(f);
		        }
		        let n = this;
		        while (n.children.length > 0) {
		            console.log(n);
		            n = n.children[0];
		        }
		        return n.appendChild(f);
		    }
            
		    return this.originalAppendChild(f);
		}
		
		bufferWindow.originalAppendChild(bufferLine)
	}
	
	/* TODO it might be better to refactor this to use the event listener overrides like most of the other effects,
	   instead of this mutation observer. */
	const callback = (mutationList, observer) => {
		window.twitchingWords = [] // make all previous text stop twitching
	    console.log(mutationList);
		for (mutation of mutationList) {
			for (addedNode of mutation.addedNodes) {
				
				/* Twitching */
				for (twitchyQuip of addedNode.querySelectorAll('.Style_user2')) {
				    twitchyQuip.innerHTML = twitchyQuip.textContent.match(/([a-z…\?!\.]+|["“”]|　) ?/g).map(word => `<span>${word}</span>`).join('');
				    for (twitchingWord of twitchyQuip.children) {
				        twitchingWord.innerHTML = twitchingWord.innerHTML.replaceAll("? ","?&zwnj; ") //last-minute hack
				        twitchingWord.innerHTML = twitchingWord.innerHTML.replaceAll("! ","!&zwnj; ")
				        wordText = twitchingWord.innerText.trim(); 
				        if (wordText=="te" || wordText=="to" || wordText=="“" || wordText=="”") {
				            twitchingWord.classList.add("teto");
				        }
				        else {
				            window.twitchingWords.push(twitchingWord);
				        }
				    }
				}
				if (window.twitchingWords.length && !window.twitchyTimeoutId) {
				    twitch();
				}
				if (!window.twitchingWords.length && window.twitchyTimeoutId) {
				    // if there aren't any active twitching words, quit calling the twitch function, for performance
				    clearTimeout(window.twitchyTimeoutId);
				    window.twitchyTimeoutId = null;
				}
			}
		}
	}

	const bufferObserver = new MutationObserver(callback);
	bufferObserver.observe(bufferWindow, {childList: true});
}, { once: true });


