package com.ProductTeam;

import java.io.IOException;
import java.util.List;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )throws IOException
    {
        Parser parse = new Parser();
        List<Question> questions =  parse.parse_questions("dataset/nfL6.json");
        QuestionResponse sampleResponse = new QuestionResponse(1, List.of(new Answer("Hello world!!", 1)));
        List<QuestionResponse> responses = List.of(sampleResponse);
        Parser.write_answers("sample_answers.json", responses);
    }
}
