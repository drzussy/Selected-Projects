package ex5.checker;

/**
 * The CompileException class represents specific exceptions that occur during the compilation of s-java code.
 * This class provides static methods to generate various predefined error messages,
 * each corresponding to a specific compilation issue such as invalid declarations,
 * comments, or method calls.
 */
public class CompileException extends Exception{

    private static final String METHOD_DOESNT_END = "method doesn't end with a 'return;' followed by a '}'";
    private static final String DOUBLE_DECLARE_METHOD_P1 = "declared method ";
    private static final String DOUBLE_DECLARE_METHOD_P2 = " again";
    private static final String INVALID_VAR_TYPE = "did not find a valid variable type";
    private static final String NO_SUCH_VAR = "did not find a valid variable identifier";
    private static final String ILLEGAL_COMMENT = "illegal comment (// not at start of line)";
    private static final String NOT_LEGAL_STATEMENT = "is not a legal statement";
    private static final String NOT_LEGAL_METHOD = "is not a legal method declaration";
    private static final String NO_SUCH_METHOD = "Called the following method but it doesn't exist: ";
    private static final String ARGS_PASSED = " arguments passed, when should pass ";

    /**
     * Constructor to initialize the CompileException with a specific error message.
     * @param errorMessage The detailed message describing the compilation error.
     */
    public CompileException(String errorMessage){
        super(errorMessage);
    }

    /**
     * Returns a CompileException for a method that doesn't end with 'return;' followed by '}'.
     * @return A CompileException indicating the method is not properly terminated.
     */
    public static CompileException methodDoesntEnd(){
        return new CompileException(METHOD_DOESNT_END);
    }
    /**
     * Returns a CompileException for a method declared twice.
     * @param methodName The name of the method that was redeclared.
     * @return A CompileException indicating duplicate method declaration.
     */
    public static CompileException doubleMethodDeclaration(String methodName){
        return new CompileException(DOUBLE_DECLARE_METHOD_P1 + methodName + DOUBLE_DECLARE_METHOD_P2);
    }
    /**
     * Returns a CompileException for an invalid variable type.
     * @return A CompileException indicating an invalid variable type.
     */
    public static CompileException invalidVarType() {
        return new CompileException(INVALID_VAR_TYPE);
    }
    /**
     * Returns a CompileException when no valid variable identifier is found.
     * @return A CompileException indicating no variable name was found.
     */
    public static CompileException noVarNameFound() {
        return new CompileException(NO_SUCH_VAR);
    }

    /**
     * Returns a CompileException for an illegal comment.
     * @return A CompileException indicating the presence of an illegal comment.
     */
    public static CompileException illegalComment() {
        return new CompileException(ILLEGAL_COMMENT);
    }

    /**
     * Returns a CompileException for an invalid or illegal statement.
     * @return A CompileException indicating the statement is not legal.
     */
    public static CompileException invalidStatement() {
        return new CompileException(NOT_LEGAL_STATEMENT);
    }

    /**
     * Returns a CompileException for an invalid method declaration.
     * @return A CompileException indicating the method declaration is not legal.
     */
    public static CompileException invalidMethodDeclaration() {
        return new CompileException(NOT_LEGAL_METHOD);
    }

    /**
     * Returns a CompileException for a method that does not exist.
     * @param methodName The name of the method that does not exist.
     * @return A CompileException indicating the method is undefined.
     */
    public static CompileException methodDoesNotExist(String methodName) {
        return new CompileException(NO_SUCH_METHOD +methodName);
    }

    /**
     * Returns a CompileException for an incorrect number of arguments passed to a method.
     * @param passed The number of arguments passed.
     * @param shouldBe The number of arguments the method expects.
     * @return A CompileException indicating the wrong number of parameters.
     */
    public static CompileException wrongParameterCount(int shouldBe, int passed) {
        return new CompileException(passed+ ARGS_PASSED +shouldBe);
    }
}
