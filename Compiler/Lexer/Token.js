const TokenType = require('./TokenType')
const AlphabeHelper = require('./AlphabetHepler')
const LexicalException = require('./LexicalException')
const arrayToGenerator = require('../common/arrayToGenerator')
const PeekIterator = require('../common/PeekIteraotr')

const KeyWords = new Set([
    'var',
    'if',
    'else',
    'for',
    'while',
    'break',
    'func',
    'return',
])


class Token {
    constructor(type, value) {
        this._type = type
        this._value = value
    }
    getValue() {
        return this._value
    }
    getType() {
        return this._type.type
    }

    isVariable() {
        return this._type == TokenType.VARIABLE
    }

    isScalar() {
        return this._type == TokenType.INTEGER ||
            this._type == TokenType.FLOAT ||
            this._type == TokenType.STRING ||
            this._type == TokenType.BOOLEAN
    }

    toString() {
        return `type ${this._type.type}, value ${this._value}`
    }

    static makeVarOrKeyWord(it) {
        let s = ""
        while (it.hasNext()) {
            const c = it.peek()
            if (AlphabeHelper.isLiteral(c)) {
                s += c
            } else {
                break
            }
            it.next()
        }
        if (KeyWords.has(s)) {
            return new Token(TokenType.KEYWORD, s)
        }
        if (s == 'true' || s == 'false') {
            return new Token(TokenType.BOOLEAN, s)
        }
        return new Token(TokenType.VARIABLE, s)
    }
    static makeString(it) {
        let s = ""
        let state = 0

        while (it.hasNext()){
            let c = it.next()
            switch(state){
                case 0:
                    if (c == '"'){
                        state = 1
                    }
                    else {
                        state = 2
                    }
                    s += c
                    break
                case 1:
                    if (c == '"'){
                        return new Token(TokenType.STRING, s + c)
                    }
                    else {
                        s += c
                    }
                    break
                case 2:
                    if (c == "'"){
                        return new Token(TokenType.STRING, s + c)
                    }
                    else {
                        s += c
                    }
                    break
            }
        }
        throw new LexicalException("Unexpected error")
    }

}
const tests = ['if']
for (let test of tests){
    const it = new PeekIterator(arrayToGenerator([...test]))
    // const token = Token.makeString(it)
    const token = Token.makeVarOrKeyWord(it)
    console.log(token.toString())
}
module.exports = Token