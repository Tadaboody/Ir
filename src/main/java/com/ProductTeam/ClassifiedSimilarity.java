package com.ProductTeam;

import org.apache.lucene.search.similarities.BasicStats;
import org.apache.lucene.search.similarities.SimilarityBase;

/**
 * ClassifiedSimilarity
 */
public class ClassifiedSimilarity extends SimilarityBase {

	@Override
	protected float score(BasicStats stats, float freq, float docLen) {
		return 0;
	}

	@Override
	public String toString() {
		return null;
	}

    
}