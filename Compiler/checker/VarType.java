package checker;

import java.util.regex.Pattern;

/**
 * enum representing the types of variables used in the language.
 * It includes types for primitive data types, variable assignment states, and type checking.
 */
enum VarType {
    /**
     * Represents a final variable that cannot be reassigned.
     */
    FINAL,

    /**
     * Represents a non-final variable that can be reassigned.
     */
    NOT_FINAL,
    /**
     * Represents the integer type.
     */
    INT,
    /**
     * Represents the double type.
     */
    DOUBLE,
    /**
     * Represents the character type.
     */
    CHAR,
    /**
     * Represents the string type.
     */
    STRING,
    /**
     * Represents the boolean type.
     */
    BOOLEAN,
    /**
     * Represents a variable that has been assigned a value.
     */
    ASSIGNED,
    /**
     * Represents a variable that has not been assigned a value.
     */
    UNASSIGNED;

    private static final Pattern INT_PATTERN = Pattern.compile("^[+-]?\\d+$");
    private static final Pattern DOUBLE_PATTERN = Pattern.compile("^[+-]?(\\d*\\.\\d+|\\d+\\.\\d*)$");
    private static final Pattern CHAR_PATTERN = Pattern.compile("^'.'$");
    private static final Pattern STRING_PATTERN = Pattern.compile("^\".*\"$");
    private static final String INT_STR = "int";
    private static final String DOUBLE_STR = "double";
    private static final String CHAR_STR = "char";
    private static final String STRING_STR = "String";
    private static final String BOOL_STR = "boolean";
    private static final String NO_SUCH_TYPE = "No matching VarType for string: ";
    private static final String ILLEGAL_VALUE = "Invalid value: ";
    private static final String TRUE_STR = "true";
    private static final String FALSE_STR = "false";
    private static final String NO_TYPE_FOUND = "No type detected for variable";

    /**
     * Converts a string representation of a type to a corresponding `VarType` enum value.
     * @param s The string representation of the type.
     * @return The corresponding `VarType`.
     * @throws IllegalSymbolException If no matching `VarType` is found.
     */
    static VarType stringTypeToVarType(String s) throws IllegalSymbolException {
        if (s == null) throw new IllegalSymbolException(NO_TYPE_FOUND);
        return switch (s) { // Using switch for cleaner code
            case INT_STR -> INT;
            case DOUBLE_STR -> DOUBLE;
            case CHAR_STR -> CHAR;
            case STRING_STR -> STRING;
            case BOOL_STR -> BOOLEAN;
            default -> throw new IllegalSymbolException(NO_SUCH_TYPE + s);
        };
    }

    /**
     * Converts a value (as a string) to its corresponding `VarType` enum value based on pattern matching.
     * @param value The value as a string.
     * @return The corresponding `VarType`.
     * @throws IllegalSymbolException If the value does not match a valid `VarType`.
     */
    static VarType valueToVarType(String value) throws IllegalSymbolException {
        if (value.equals(TRUE_STR) || value.equals(FALSE_STR)) return BOOLEAN;
        else if (CHAR_PATTERN.matcher(value).matches()) return CHAR;
        else if (STRING_PATTERN.matcher(value).matches()) return STRING;
        else if (INT_PATTERN.matcher(value).matches()) return INT;
        else if (DOUBLE_PATTERN.matcher(value).matches()) return DOUBLE;
        throw new IllegalSymbolException(ILLEGAL_VALUE + value);
    }

    /**
     * Checks/defines if assigning one `VarType` to another is legal based on the language's assignment rules.
     * @param receiver The type of the variable being assigned to.
     * @param giver The type of the value being assigned.
     * @throws IllegalSymbolException If the assignment is illegal.
     */
    static void checkLegalAssignment(VarType receiver, VarType giver)
            throws IllegalSymbolException {
        if (receiver==giver) return;
        boolean giverCondition = giver==VarType.INT || giver==VarType.DOUBLE;
        boolean receiverCondition = receiver==VarType.BOOLEAN || receiver==VarType.DOUBLE;
//      int->boolean: allowed, int->double: allowed, double->boolean: allowed, double->double: allowed (duh)
//      and no other cases are allowed, so these conditions cover everything.
        if (giverCondition && receiverCondition) return;
        throw IllegalSymbolException.illegalAssignment(receiver.name(), giver.name());
    }
}
