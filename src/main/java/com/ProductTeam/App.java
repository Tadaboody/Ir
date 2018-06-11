package com.ProductTeam;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.RAMDirectory;

/**
 * Hello world!
 *
 */
public class App {

    public static final String TEST_QUESTION = "2311395	Whenever the batterys are low on somebody's remote, why do they just press the buttons even harder?";

    public static void main(String[] args) throws Exception {

        try (Directory dir = newDirectory(); Analyzer analyzer = newAnalyzer()) {
            // Index
            index(dir, analyzer);
            List<QuestionResponse> responses = new ArrayList<>();
            Iterable<String> readFile = readFile(args[0]);
            for (String query_string : readFile) {
                responses.add(search(query_string, dir, analyzer));
            }
            Parser.write_answers("results.json", responses);
        }
    }

    private static Iterable<String> readFile(String path) throws IOException {
        try (BufferedReader reader = new BufferedReader(new FileReader(path))) {
            return reader.lines().collect(Collectors.toList());
        }
    }

    private static QuestionResponse search(String query_string, Directory dir, Analyzer analyzer)
            throws IOException, ParseException {
        int question_id = RegexHelper.parse_question_id(query_string);
        query_string = RegexHelper.parse_question_string(query_string);

        final QueryParser parser = new QueryParser(Answer.BODY_FIELD, analyzer);
        try (DirectoryReader reader = DirectoryReader.open(dir)) {
            final Query query = parser.parse(QueryParser.escape(query_string));
            final IndexSearcher searcher = new IndexSearcher(reader);
            final AnswerSearcher answerSearcher = new BestAnswerSearcher();
            final List<Answer> answers = answerSearcher.search(searcher, query);
            final QuestionResponse response = new QuestionResponse(question_id, answers);
            return response;
        }
    }

    private static void index(Directory dir, Analyzer analyzer) throws IOException {
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
