package com.ProductTeam;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        Parser parse = new Parser();
        System.out.println(parse.parse_questions("dataset/nfL6.json").get(0));
    }
}
