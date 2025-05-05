package checker;

/**
 * The IllegalSymbolException class represents exceptions related to invalid operations
 * involving symbols (e.g., variables) in the s-java code. This includes usage of undefined
 * or uninitialized variables, re-declaration errors, illegal assignments, and issues with final variables.
 */
public class IllegalSymbolException extends CompileException {
    private static final String NO_SUCH_VAR = "Tried using value of nonexistent variable ";
    private static final String UNASSIGNED_VAR = "Attempted using value of unassigned variable ";
    private static final String REDECLARED_VAR = "Tried re-declaring variable in current scope: ";
    private static final String ASSIGN_TO_FINAL = "Attempted assignment to final variable ";
    private static final String ILLEGAL_ASSIGN = " illegally assigned to a ";
    private static final String FINAL_NO_INIT = " was declared final without initialization";
    private static final String RESERVED_KEYWORD = " is not a valid variable name";
    private static final String NO_TABLE = " tried returning a local scope snapshot but none found";
    private static final String NULL_SNAPSHOT = " cannot restore scope from a null snapshot";

    /**
     * Constructor to initialize the IllegalSymbolException with a specific error message.
     * @param errorMessage The detailed message describing the illegal symbol operation.
     */
    public IllegalSymbolException (String errorMessage) {
        super(errorMessage);
    }

    /**
     * Returns an IllegalSymbolException for using a variable that does not exist.
     * @param varName The name of the nonexistent variable.
     * @return An IllegalSymbolException indicating the variable was not found.
     */
    public static IllegalSymbolException symbolNotFound(String varName){
        return new IllegalSymbolException(NO_SUCH_VAR + varName);
    }

    /**
     * Returns an IllegalSymbolException for using an unassigned variable.
     * @param varName The name of the unassigned variable.
     * @return An IllegalSymbolException indicating the variable was not assigned a value.
     */
    public static IllegalSymbolException unassignedUsage(String varName){
        return new IllegalSymbolException(UNASSIGNED_VAR + varName);
    }
    /**
     * Returns an IllegalSymbolException for attempting to re-declare a variable in the current scope.
     * @param varName The name of the variable being re-declared.
     * @return An IllegalSymbolException indicating the variable already exists.
     */
    public static IllegalSymbolException varAlreadyExists(String varName){
        return new IllegalSymbolException(REDECLARED_VAR + varName);
    }

    /**
     * Returns an IllegalSymbolException for attempting to assign a value to a final variable.
     * @param varName The name of the final variable.
     * @return An IllegalSymbolException indicating assignment to a final variable is not allowed.
     */
    public static IllegalSymbolException assignmentToFinalVar(String varName) {
        return new IllegalSymbolException(ASSIGN_TO_FINAL + varName);
    }

    /**
     * Returns an IllegalSymbolException for performing an illegal assignment between types.
     * @param assignedType The type being assigned to.
     * @param assigningType The type being assigned.
     * @return An IllegalSymbolException indicating an invalid type assignment.
     */
    public static IllegalSymbolException illegalAssignment(String assignedType, String assigningType) {
        return new IllegalSymbolException(assigningType + ILLEGAL_ASSIGN + assignedType);
    }

    /**
     * Returns an IllegalSymbolException for declaring a final variable without initialization.
     * @param varName The name of the final variable.
     * @return An IllegalSymbolException indicating the final variable was not initialized.
     */
    public static IllegalSymbolException uninitializedFinalVar(String varName){
        return new IllegalSymbolException(varName + FINAL_NO_INIT);
    }

    /**
     * Returns an IllegalSymbolException for using an illegal variable name that contains
     * a reserved keyword.
     *
     * @param varName The name of the variable that caused the exception.
     * @return An IllegalSymbolException indicating the variable name is illegal due to
     *         containing a reserved keyword.
     */
    public static IllegalSymbolException illegalVarName (String varName) {
        return new IllegalSymbolException(varName + RESERVED_KEYWORD);
    }

    /**
     * Returns an IllegalSymbolException for using getLocalSnapshot() when there isn't a local scope.
     * @return An IllegalSymbolException indicating the local scope does not exist.
     */
    public static IllegalSymbolException noLocalTableFound(){
        return new IllegalSymbolException(NO_TABLE);
    }

    /**
     * Returns an IllegalSymbolException for attempting to restore a scope from a null Snapshot.
     * @return An IllegalSymbolException detailing the passed Snapshot is null.
     */
    public static IllegalSymbolException noSnapshotGiven() {
        return new IllegalSymbolException(NULL_SNAPSHOT);
    }
}
