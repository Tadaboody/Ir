package com.ProductTeam;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
import java.io.Writer;
import java.util.ArrayList;
import java.util.List;

import com.google.common.reflect.TypeToken;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.stream.JsonReader;

class Parser
{
    private static final String DATASET_PATH = "dataset/nfL6.json";

	public static List<Question> parse_questions(String path) throws IOException
    {
        Gson gson_parser = new Gson();
        try (Reader fp = new FileReader(path)) {
            JsonReader reader = new JsonReader(fp);
            return gson_parser.fromJson(reader, new TypeToken<ArrayList<Question>>() {
            }.getType());
        }
    }

    /**
     * A useful alias for quickly parsing the core dataset
     */
    public static List<Question> parse_dataset() throws IOException
    {
        return Parser.parse_questions(DATASET_PATH);
    }

    public static void write_answers(String path,List<QuestionResponse> responses) throws IOException
    {
        Gson gson = new GsonBuilder()
        .setPrettyPrinting()
        .disableHtmlEscaping()
        .create();
        try(Writer fp = new FileWriter(path))
        {
            gson.toJson(responses, new ArrayList<QuestionResponse>().getClass(), fp);
        }
    }
}