package ex5.checker;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Pattern;

/**
 * This package-protected class manages a symbol table for variable declarations, assignments,
 * and type checking in the context of variable scoping.<br>
 * It supports operations for entering/exiting scopes, declaring variables,
 * and ensuring legal variable assignments.
 */
class SymbolTable{
    private static final String FINALITY = "isFinal";
    private static final String TYPE = "type";
    private static final String ASSIGNMENT = "isAssigned";
    private static final Pattern TRUE_OR_FALSE_PATTERN = Pattern.compile("true|false");
    private static class VariableDescription extends HashMap<String, VarType> {
        private VariableDescription (VariableDescription other) {
            super(other);
        }
        private VariableDescription (VarType isFinal, VarType type, VarType isAssigned){
            put(FINALITY, isFinal);
            put(TYPE, type);
            put(ASSIGNMENT, isAssigned);
        }
    }
    /*
     * Represents a table of variables and their descriptions (finality, type, and assignment status).
     */
    private static class VariableTable extends HashMap<String, VariableDescription> {
        private VariableTable () {}
        private VariableTable (VariableTable other) {
            super();
            for (HashMap.Entry<String, VariableDescription> entry : other.entrySet()) {
                this.put(entry.getKey(), new VariableDescription(entry.getValue()));
            }
        }
    }

    /**
     * Represents a snapshot of a single scope - either global or local - implementing the
     * Memento design pattern. Created via getGlobalSnapshot() / getLocalSnapshot(),
     * and used via restoreGlobalSnapshot() / restoreLocalSnapshot().
     */
    static class Snapshot {
        private final VariableTable tableSnapshot;
        private Snapshot (VariableTable tableToSave) {
            tableSnapshot = new VariableTable(tableToSave);
        }
    }
    private VariableTable globalTable = new VariableTable();
    private final ArrayList<VariableTable> scopeTables = new ArrayList<>();

    // default constructor

    /**
     * Retrieves a snapshot of the global variable table.
     * @return A copy of the global variable table.
     */
    Snapshot getGlobalSnapshot() {
        return new Snapshot(globalTable);
    }
    /**
     * Restores the global variable table to the provided snapshot,
     * <b>OVERRIDING the current global scope.</b>
     * @param toRestore The snapshot of the global table to restore.
     */
    void restoreGlobalSnapshot(Snapshot toRestore) throws IllegalSymbolException {
        if (toRestore==null) throw IllegalSymbolException.noSnapshotGiven();
        globalTable = new VariableTable(toRestore.tableSnapshot);
    }

    /**
     * Retrieves a snapshot of the local variable table.
     * @return A copy of the local variable table.
     */
    Snapshot getLocalSnapshot() throws IllegalSymbolException {
        if (scopeTables.isEmpty()) throw IllegalSymbolException.noLocalTableFound();
        return new Snapshot(scopeTables.get(scopeTables.size()-1));
    }

    /**
     * Restores the current local variable table to the provided snapshot,
     * <b>ADDING this as the new innermost local scope</b> (not overriding the existing one).
     * @param toRestore The snapshot of the local table to restore.
     * If null is provided, a new scope is entered.
     */
    void restoreLocalSnapshot(Snapshot toRestore) throws IllegalSymbolException {
        if (toRestore==null) throw IllegalSymbolException.noSnapshotGiven();
        scopeTables.add(new VariableTable(toRestore.tableSnapshot));
    }

    /**
     * Enters a new scope by adding a new local variable table.
     */
    void enterScope() {
        scopeTables.add(new VariableTable());
    }

    /**
     * Exits the current scope by removing the topmost local variable table.
     */
    void exitScope() {
        scopeTables.remove(scopeTables.size()-1);
    }

    /**
     * Assigns a value to an existing variable, ensuring the variable is not final
     * and the assignment is legal based on its declared type.
     * @param varName The name of the variable.
     * @param assigningType The type of the value being assigned.
     * @throws IllegalSymbolException If the variable is final or the assignment is illegal.
     */
    void assignToVar(String varName, VarType assigningType) throws IllegalSymbolException {
        VariableDescription desc = findVar(varName);
        if (desc.get(FINALITY)==VarType.FINAL) throw IllegalSymbolException.assignmentToFinalVar(varName);
        VarType varType = desc.get(TYPE);
        VarType.checkLegalAssignment(varType, assigningType);
        desc.replace(ASSIGNMENT, VarType.ASSIGNED);
    }

    /**
     * Retrieves the type of a variable if it has been assigned a value.
     * @param varName The name of the variable.
     * @return The type of the variable.
     * @throws IllegalSymbolException If the variable has not been assigned a value.
     */
    VarType getVariableTypeIfAssigned(String varName) throws IllegalSymbolException {
        VariableDescription desc = findVar(varName); // if varName not assigned - throws exception
        if (desc.get(ASSIGNMENT)==VarType.UNASSIGNED) throw IllegalSymbolException.unassignedUsage(varName);
        return desc.get(TYPE);
    }

    /**
     * Declares a new variable with a specified finality, type, and unassigned status.
     * @param varName The name of the variable.
     * @param finality The finality of the variable.
     * @param type The type of the variable.
     * @throws IllegalSymbolException If the variable already exists.
     */
    void declareVar(String varName, VarType finality, VarType type) throws IllegalSymbolException {
        VariableTable currentTable = checkVarAndGetCurrentTable(varName);
        if (finality==VarType.FINAL) throw IllegalSymbolException.uninitializedFinalVar(varName);
        currentTable.put(varName, new VariableDescription(finality, type, VarType.UNASSIGNED));
    }

    /**
     * Declares a new variable with a specified finality, assigned type, and assigned value type.
     * @param varName The name of the variable.
     * @param finality The finality of the variable.
     * @param declaredType The type of the variable once assigned.
     * @param assigningType The type of the value being assigned.
     * @throws IllegalSymbolException If the variable already exists or the assignment is illegal.
     */
    void declareVar(String varName, VarType finality, VarType declaredType, VarType assigningType)
            throws IllegalSymbolException {
        VarType.checkLegalAssignment(declaredType, assigningType);
        VariableTable currentTable = checkVarAndGetCurrentTable(varName);
        currentTable.put(varName, new VariableDescription(finality, declaredType, VarType.ASSIGNED));
    }

    /**
     * Declares a parameter with a specified finality, type, and assigned status.
     * @param varName The name of the parameter.
     * @param finality The finality of the parameter.
     * @param type The type of the parameter.
     * @throws IllegalSymbolException If the parameter already exists.
     */
    void declareParameter(String varName, VarType finality, VarType type) throws IllegalSymbolException {
        VariableTable currentTable = checkVarAndGetCurrentTable(varName);
        currentTable.put(varName, new VariableDescription(finality, type, VarType.ASSIGNED));
    }

    private VariableTable checkVarAndGetCurrentTable(String varName) throws IllegalSymbolException {
        if (TRUE_OR_FALSE_PATTERN.matcher(varName).matches()) {
            throw IllegalSymbolException.illegalVarName(varName);
        }
        VariableTable currentTable = globalTable;
        if (!scopeTables.isEmpty()) currentTable = scopeTables.get(scopeTables.size()-1);
        VariableDescription desc = currentTable.get(varName);
        if (desc!=null) throw IllegalSymbolException.varAlreadyExists(varName);
        return currentTable;
    }

    private VariableDescription findVar (String varName) throws IllegalSymbolException {
        VariableDescription varDesc;
        for (int i = scopeTables.size()-1; i >= 0; i--) {
            varDesc = scopeTables.get(i).get(varName);
            if (varDesc!=null) return varDesc;
        }
        varDesc = globalTable.get(varName);
        if (varDesc==null) throw IllegalSymbolException.symbolNotFound(varName);
        return varDesc;
    }

}
