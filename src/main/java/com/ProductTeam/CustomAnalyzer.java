package com.ProductTeam;

import org.apache.commons.codec.language.Soundex;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.LowerCaseFilter;
import org.apache.lucene.analysis.StopFilter;
import org.apache.lucene.analysis.TokenStream;
import org.apache.lucene.analysis.Tokenizer;
import org.apache.lucene.analysis.en.EnglishPossessiveFilter;
import org.apache.lucene.analysis.en.PorterStemFilter;
import org.apache.lucene.analysis.phonetic.PhoneticFilter;
import org.apache.lucene.analysis.phonetic.PhoneticFilterFactory;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.standard.StandardFilter;
import org.apache.lucene.analysis.standard.StandardTokenizer;

/**
 * CustomAnalyzer
 */
public class CustomAnalyzer extends Analyzer {

    private static class DefaultSetHolder {
        static final CharArraySet DEFAULT_STOP_SET = StandardAnalyzer.STOP_WORDS_SET;
    }

    public static CharArraySet getDefaultStopSet() {
        return DefaultSetHolder.DEFAULT_STOP_SET;
    }

    @Override
    protected TokenStreamComponents createComponents(String fieldName) {
        final Tokenizer source = new StandardTokenizer();
        TokenStream result = new StandardFilter(source);
        result = new EnglishPossessiveFilter(result);
        result = new LowerCaseFilter(result);
        result = new StopFilter(result, getDefaultStopSet());
        result = new PorterStemFilter(result);
        result = new PhoneticFilter(result,new Soundex(),false);
        return new TokenStreamComponents(source, result);
    }
}