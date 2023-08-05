define("ace/mode/batchfile_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"], function(require, exports, module) {
"use strict";

var oop = require("../lib/oop");
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;

var BatchFileHighlightRules = function() {

    this.$rules = { start: 
       [ { token: 'keyword.command.dosbatch',
           regex: '\\b(?:append|assoc|at|attrib|break|cacls|cd|chcp|chdir|chkdsk|chkntfs|cls|cmd|color|comp|compact|convert|copy|date|del|dir|diskcomp|diskcopy|doskey|echo|endlocal|erase|fc|find|findstr|format|ftype|graftabl|help|keyb|label|md|mkdir|mode|more|move|path|pause|popd|print|prompt|pushd|rd|recover|ren|rename|replace|restore|rmdir|set|setlocal|shift|sort|start|subst|time|title|tree|type|ver|verify|vol|xcopy)\\b',
           caseInsensitive: true },
         { token: 'keyword.control.statement.dosbatch',
           regex: '\\b(?:goto|call|exit)\\b',
           caseInsensitive: true },
         { token: 'keyword.control.conditional.if.dosbatch',
           regex: '\\bif\\s+not\\s+(?:exist|defined|errorlevel|cmdextversion)\\b',
           caseInsensitive: true },
         { token: 'keyword.control.conditional.dosbatch',
           regex: '\\b(?:if|else)\\b',
           caseInsensitive: true },
         { token: 'keyword.control.repeat.dosbatch',
           regex: '\\bfor\\b',
           caseInsensitive: true },
         { token: 'keyword.operator.dosbatch',
           regex: '\\b(?:EQU|NEQ|LSS|LEQ|GTR|GEQ)\\b' },
         { token: ['doc.comment', 'comment'],
           regex: '(?:^|\\b)(rem)($|\\s.*$)',
           caseInsensitive: true },
         { token: 'comment.line.colons.dosbatch',
           regex: '::.*$' },
         { include: 'variable' },
         { token: 'punctuation.definition.string.begin.shell',
           regex: '"',
           push: [ 
              { token: 'punctuation.definition.string.end.shell', regex: '"', next: 'pop' },
              { include: 'variable' },
              { defaultToken: 'string.quoted.double.dosbatch' } ] },
         { token: 'keyword.operator.pipe.dosbatch', regex: '[|]' },
         { token: 'keyword.operator.redirect.shell',
           regex: '&>|\\d*>&\\d*|\\d*(?:>>|>|<)|\\d*<&|\\d*<>' } ],
        variable: [
         { token: 'constant.numeric', regex: '%%\\w+|%[*\\d]|%\\w+%'},
         { token: 'constant.numeric', regex: '%~\\d+'},
         { token: ['markup.list', 'constant.other', 'markup.list'],
            regex: '(%)(\\w+)(%?)' }]}
    
    this.normalizeRules();
};

BatchFileHighlightRules.metaData = { name: 'Batch File',
      scopeName: 'source.dosbatch',
      fileTypes: [ 'bat' ] }


oop.inherits(BatchFileHighlightRules, TextHighlightRules);

exports.BatchFileHighlightRules = BatchFileHighlightRules;
});

define("ace/mode/folding/cstyle",["require","exports","module","ace/lib/oop","ace/range","ace/mode/folding/fold_mode"], function(require, exports, module) {
"use strict";

var oop = require("../../lib/oop");
var Range = require("../../range").Range;
var BaseFoldMode = require("./fold_mode").FoldMode;

var FoldMode = exports.FoldMode = function(commentRegex) {
    if (commentRegex) {
        this.foldingStartMarker = new RegExp(
            this.foldingStartMarker.source.replace(/\|[^|]*?$/, "|" + commentRegex.start)
        );
        this.foldingStopMarker = new RegExp(
            this.foldingStopMarker.source.replace(/\|[^|]*?$/, "|" + commentRegex.end)
        );
    }
};
oop.inherits(FoldMode, BaseFoldMode);

(function() {

    this.foldingStartMarker = /(\{|\[)[^\}\]]*$|^\s*(\/\*)/;
    this.foldingStopMarker = /^[^\[\{]*(\}|\])|^[\s\*]*(\*\/)/;

    this.getFoldWidgetRange = function(session, foldStyle, row, forceMultiline) {
        var line = session.getLine(row);
        var match = line.match(this.foldingStartMarker);
        if (match) {
            var i = match.index;

            if (match[1])
                return this.openingBracketBlock(session, match[1], row, i);
                
            var range = session.getCommentFoldRange(row, i + match[0].length, 1);
            
            if (range && !range.isMultiLine()) {
                if (forceMultiline) {
                    range = this.getSectionRange(session, row);
                } else if (foldStyle != "all")
                    range = null;
            }
            
            return range;
        }

        if (foldStyle === "markbegin")
            return;

        var match = line.match(this.foldingStopMarker);
        if (match) {
            var i = match.index + match[0].length;

            if (match[1])
                return this.closingBracketBlock(session, match[1], row, i);

            return session.getCommentFoldRange(row, i, -1);
        }
    };
    
    this.getSectionRange = function(session, row) {
        var line = session.getLine(row);
        var startIndent = line.search(/\S/);
        var startRow = row;
        var startColumn = line.length;
        row = row + 1;
        var endRow = row;
        var maxRow = session.getLength();
        while (++row < maxRow) {
            line = session.getLine(row);
            var indent = line.search(/\S/);
            if (indent === -1)
                continue;
            if  (startIndent > indent)
                break;
            var subRange = this.getFoldWidgetRange(session, "all", row);
            
            if (subRange) {
                if (subRange.start.row <= startRow) {
                    break;
                } else if (subRange.isMultiLine()) {
                    row = subRange.end.row;
                } else if (startIndent == indent) {
                    break;
                }
            }
            endRow = row;
        }
        
        return new Range(startRow, startColumn, endRow, session.getLine(endRow).length);
    };

}).call(FoldMode.prototype);

});

define("ace/mode/batchfile",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/batchfile_highlight_rules","ace/mode/folding/cstyle"], function(require, exports, module) {
"use strict";

var oop = require("../lib/oop");
var TextMode = require("./text").Mode;
var BatchFileHighlightRules = require("./batchfile_highlight_rules").BatchFileHighlightRules;
var FoldMode = require("./folding/cstyle").FoldMode;

var Mode = function() {
    this.HighlightRules = BatchFileHighlightRules;
    this.foldingRules = new FoldMode();
};
oop.inherits(Mode, TextMode);

(function() {
    this.lineCommentStart = "::";
    this.blockComment = "";
    this.$id = "ace/mode/batchfile";
}).call(Mode.prototype);

exports.Mode = Mode;
});
