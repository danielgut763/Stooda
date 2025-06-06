package org.stooda.model;

import java.time.LocalDate;
import java.util.List;

public class Question {
    private QuestionText questionText;
    private List<Alternative> alternatives;
    private Subject subject;
    private ExamType examType;
    private LocalDate data;
    private Difficulty difficulty;
}
