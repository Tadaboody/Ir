package com.ProductTeam;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * RegexHelper
 */

public class RegexHelper {

    public static String get_query_group(String query_string, int groupNum) {
        final String REGEX_PATTERN = "(\\d+)\\s(.+)";
        final Pattern REGEX = Pattern.compile(REGEX_PATTERN, Pattern.MULTILINE);
        Matcher matcher = REGEX.matcher(query_string);
        matcher.find();
        return matcher.group(groupNum);
    }

    public static String parse_question_id(String query_string) {
        return get_query_group(query_string, 1);
    }

    public static String parse_question_string(String query_string) {
        return get_query_group(query_string, 2);
    }

}