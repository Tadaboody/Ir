package com.ProductTeam;

import java.io.IOException;
import java.text.ParseException;
import java.util.List;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.Query;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )throws Exception
    {
        String query_string = args[0];
        try (Directory dir = newDirectory();
                Analyzer analyzer = newAnalyzer()) {
            // Index
            index(dir, analyzer);
            search(query_string, dir, analyzer);
        }
    }

    private static void search(String query_string,Directory dir, Analyzer analyzer) throws IOException,org.apache.lucene.queryparser.classic.ParseException
    {
        final QueryParser parser = new QueryParser(Answer.BODY_FIELD, analyzer);
        try (DirectoryReader reader = DirectoryReader.open(dir)) {
            final Query query = parser.parse(query_string);
        }
    }

    private static void index(Directory dir, Analyzer analyzer)throws IOException
    {
        List<Question> dataset = Parser.parse_dataset();
        try (IndexWriter writer = new BasicIndexWriter(dir, analyzer)) {
            for (final Question question : dataset) {
                writer.addDocuments(question.answerDocuments());
            }
        }
    }

    private static Directory newDirectory() {
        return new RAMDirectory();
    }

    private static Analyzer newAnalyzer() {
        return new EnglishAnalyzer();
    }
}
