package com.ProductTeam;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.Analyzer.TokenStreamComponents;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.deeplearning4j.text.tokenization.tokenizerfactory.DefaultTokenizerFactory;
import org.deeplearning4j.text.tokenization.tokenizerfactory.TokenizerFactory;
import org.deeplearning4j.text.tokenization.tokenizer.preprocessor.CommonPreprocessor;
/**
 * Word2VecAnalyzer
 */
public class Word2VecAnalyzer extends Analyzer{

    private Analyzer innerAnalyzer = new EnglishAnalyzer();
	@Override
	protected TokenStreamComponents createComponents(String fieldName) {
        TokenizerFactory t = new DefaultTokenizerFactory();
        t.setTokenPreProcessor(new CommonPreprocessor());
        innerAnalyzer.getOffsetGap(fieldName);
		return null;
	}

    
}