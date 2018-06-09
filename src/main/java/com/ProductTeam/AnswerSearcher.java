package com.ProductTeam;

import java.util.List;

import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;

/**
 * AnswerSearcher
 */
public interface AnswerSearcher {

    public List<Answer> search(IndexSearcher searcher, Query query);
}