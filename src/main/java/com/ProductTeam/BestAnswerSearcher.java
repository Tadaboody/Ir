package com.ProductTeam;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.lucene.document.Document;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;

/**
 * BestAnswerSearcher
 */
public class BestAnswerSearcher  implements AnswerSearcher{

	@Override
	public List<Answer> search(IndexSearcher searcher, Query query) throws IOException {
        final int n = 5;
        final TopDocs topDocs = searcher.search(query, n);
        final List<Answer> answers = new ArrayList<>();
        for (ScoreDoc scoreDoc : topDocs.scoreDocs) {
            final Document doc = searcher.doc(scoreDoc.doc);
            answers.add(Answer.fromDocAnswer(doc, scoreDoc.score));
        }
        return answers;
    }

}