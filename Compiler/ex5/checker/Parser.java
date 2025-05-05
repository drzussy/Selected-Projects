package ex5.checker;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * The Parser class is responsible for checker and validating S-Java code files.
 * It ensures the correctness of syntax, variable declarations, assignments,
 * method definitions, and other code constructs.
 */
public class Parser {
    private static final Pattern RETURN_PATTERN = Pattern.compile("return\\s*;");
    private static final Pattern VOID_PATTERN = Pattern.compile("void .*");
    private static final Pattern FINAL_PATTERN = Pattern.compile("final");
    private static final Pattern OPEN_CURLY_END_PATTERN = Pattern.compile(".*\\{$");
    private static final Pattern CLOSE_CURLY_PATTERN = Pattern.compile("}");
    private static final Pattern ILLEGAL_COMMENT_PATTERN = Pattern.compile("[^/]+//.*}");
    private static final Pattern COMMENT_PATTERN = Pattern.compile("//.*");
    private static final String VAR_NAME_REGEX = "((?:_[a-zA-Z0-9]|[a-zA-Z])\\w*)"; // Note: captures name
    private static final String VAR_TYPE_REGEX = "(int|double|String|boolean|char)"; // Note: captures type
    private static final String VALUE_REGEX = "(true|false|'.'|\".*\"|[+-]?[.\\d]+|"+VAR_NAME_REGEX+")";
                // Note: captures value
    private static final Pattern VAR_TYPE_PATTERN = Pattern.compile(VAR_TYPE_REGEX);
    private static final Pattern VALUE_PATTERN = Pattern.compile(VALUE_REGEX);
    private static final String ASSIGNMENT_REGEX = VAR_NAME_REGEX+"\\s*=\\s*"+VALUE_REGEX;
    private static final Pattern ASSIGNMENT_PATTERN = Pattern.compile(ASSIGNMENT_REGEX);
                // captures one assignment at a time
    private static final String NAME_AND_MAYBE_ALSO_VALUE_REGEX =
            VAR_NAME_REGEX + "\\s*(?:=\\s*"+VALUE_REGEX+")?\\s*";
    private static final Pattern DECLARE_PATTERN = Pattern.compile(NAME_AND_MAYBE_ALSO_VALUE_REGEX);
    private static final String DECLARE_LINE_REGEX =
            "^(final\\s+)?"+VAR_TYPE_REGEX+"\\s+"+ NAME_AND_MAYBE_ALSO_VALUE_REGEX +
                    "(,\\s*"+ NAME_AND_MAYBE_ALSO_VALUE_REGEX +")*\\s*;$";
    private static final String ASSIGN_LINE_REGEX =
            "^"+ASSIGNMENT_REGEX+"(,"+ASSIGNMENT_REGEX+")*;$";
    private static final Pattern ASSIGN_LINE_PATTERN = Pattern.compile(ASSIGN_LINE_REGEX);
    private static final Pattern DECLARE_LINE_PATTERN = Pattern.compile(DECLARE_LINE_REGEX);
    private static final String METHOD_NAME_REGEX = "([a-zA-Z]\\w*)"; // Note: captures name
    private static final Pattern METHOD_CALL_PATTERN = Pattern.compile(
                    METHOD_NAME_REGEX+"\\s*\\((.*)\\)\\s*;");
    private static final String SINGLE_PARAMETER_REGEX =
            "(?:(final)\\s+)?"+VAR_TYPE_REGEX+"\\s+"+VAR_NAME_REGEX;
    private static final Pattern PARAMETER_PATTERN = Pattern.compile(SINGLE_PARAMETER_REGEX);
    private static final String PARAMETER_LIST_REGEX =
            SINGLE_PARAMETER_REGEX + "(?:\\s*,\\s*" + SINGLE_PARAMETER_REGEX + ")*";
    private static final Pattern METHOD_DEFINE_PATTERN = Pattern.compile(
        "^void\\s+" + METHOD_NAME_REGEX + "\\s*\\(\\s*(" + PARAMETER_LIST_REGEX+")?\\s*\\)\\s*\\{$");
    private static final String FULL_CONDITION_REGEX =
            "(\\s*"+VALUE_REGEX+"(?:\\s*(?:\\|\\||&&)\\s*"+VALUE_REGEX+")*\\s*)\\s*";
    private static final String FLOW_STATEMENT_REGEX =
                    "^(?:if|while)\\s*\\("+FULL_CONDITION_REGEX+"\\)\\s*\\{$";
    private static final Pattern FLOW_KEYWORD_PATTERN = Pattern.compile(FLOW_STATEMENT_REGEX);

    private static final int SECOND_GROUP=2;
    private static final int THIRD_GROUP = 3;
    private HashMap<String, List<String>> methodsList;
    private HashMap<String, ArrayList<VarType>> methodsParameters;
    private HashMap<String, Integer> methodStartLines;
    private HashMap<String, SymbolTable.Snapshot> methodStartingScopes;
    private BufferedReader reader;
    private SymbolTable symbolTable;
    private int curLineNum=0;

    /**
     * Constructs a new Parser instance.
     */
    public Parser() {}

    /**
     * Returns the current line number being processed by the parser.
     *
     * @return the current line number.
     */
    public int getCurrentLine () {
        return curLineNum;
    }

    /**
     * Parses the given file and checks if it contains legal S-Java code.
     *
     * @param bufferedReader the buffered reader providing the file content.
     * @throws IOException                   if an I/O error occurs.
     * @throws CompileException              if a compile-time error is detected.
     * @throws IllegalSymbolException        if an illegal symbol or variable is encountered.
     */
    public void parseFile(BufferedReader bufferedReader)
            throws IOException, CompileException, IllegalSymbolException {
        this.reader = bufferedReader;
        String line;
        symbolTable = new SymbolTable(); // reset symbol table
        methodsParameters = new HashMap<>();
        methodStartLines = new HashMap<>();
        methodStartingScopes = new HashMap<>();
        // (symbol table is reset here and not in constructor, to allow for checker multiple files)
        this.methodsList = new HashMap<>();
        //iterate through buffer and until finished, add each line to the line list
        while ((line = reader.readLine()) != null){
            curLineNum++;
            if (ILLEGAL_COMMENT_PATTERN.matcher(line).matches()) throw CompileException.illegalComment();
            if (!COMMENT_PATTERN.matcher(line).matches()) { // if line is a legal comment - skip
                line = line.strip(); // get rid of leading/trailing whitespace when it's in a legal setting
                if (line.isEmpty()) continue;
                if (VOID_PATTERN.matcher(line).matches()) copyMethodToMethodList(line); // void <-> method
                else parseVarStatement(line); // otherwise, parse as a (global) var statement
            }
        }
        SymbolTable.Snapshot globalSnapshot = symbolTable.getGlobalSnapshot();
        for (String methodName: methodsList.keySet()) {
            curLineNum = methodStartLines.get(methodName);
            SymbolTable.Snapshot currentScope = methodStartingScopes.get(methodName);
            symbolTable.restoreLocalSnapshot(currentScope);
            parseMethod(methodsList.get(methodName));
            symbolTable.exitScope();
            symbolTable.restoreGlobalSnapshot(globalSnapshot);
        }
    }

    private void parseVarStatement(String line) throws CompileException {
        if (DECLARE_LINE_PATTERN.matcher(line).matches()) {
            Matcher typeFinder = VAR_TYPE_PATTERN.matcher(line);
            if (!typeFinder.find()) throw CompileException.invalidVarType();
            VarType type = VarType.stringTypeToVarType(typeFinder.group());
            Matcher varFinder = DECLARE_PATTERN.matcher(line);
            if (!varFinder.find()) throw CompileException.noVarNameFound();
            VarType finality = VarType.NOT_FINAL;
            if (FINAL_PATTERN.matcher(varFinder.group()).find()) {
               finality = VarType.FINAL;
               varFinder.find(); // skip over to var type
            }
            while (varFinder.find()) { // skip over var type
                String varName = varFinder.group(1);
                String value = varFinder.group(SECOND_GROUP);
                if (value!=null) {
                    if (value.equals(varName)) throw IllegalSymbolException.unassignedUsage(varName);
                    VarType valueType = getVarTypeFromValue(value);
                    symbolTable.declareVar(varName, finality, type, valueType);
                } else symbolTable.declareVar(varName, finality, type);
            }
        }
        else if (ASSIGN_LINE_PATTERN.matcher(line).matches()) {
            Matcher assignmentFinder = ASSIGNMENT_PATTERN.matcher(line);
            while (assignmentFinder.find()) { // skip over var type
                String varName = assignmentFinder.group(1);
                String value = assignmentFinder.group(SECOND_GROUP);
                VarType valueType = getVarTypeFromValue(value);
                symbolTable.assignToVar(varName, valueType);
            }
        }
        else throw CompileException.invalidStatement();
    }

    private void copyMethodToMethodList(String line)
            throws CompileException, IOException {
        Matcher methodDeclarationMatcher = METHOD_DEFINE_PATTERN.matcher(line);
        if (!methodDeclarationMatcher.matches()) throw CompileException.invalidMethodDeclaration();
        String methodName = methodDeclarationMatcher.group(1);
        if (methodStartLines.containsKey(methodName)) throw CompileException.doubleMethodDeclaration(
                                                                                            methodName);
        methodStartLines.put(methodName, curLineNum);
        ArrayList<VarType> paramList = parseParamList(
                methodDeclarationMatcher.group(SECOND_GROUP), methodName);
        methodsParameters.put(methodName, paramList);
        List<String> method = new ArrayList<>();
        int scope = 1;
        while ((line = reader.readLine()) != null) {
            if (ILLEGAL_COMMENT_PATTERN.matcher(line).matches()) throw CompileException.illegalComment();
            curLineNum++;
            line = line.strip();
            if (line.isEmpty() || COMMENT_PATTERN.matcher(line).matches()) {
                method.add(""); // add empty line for line counting logic
                continue;
            }
            if (OPEN_CURLY_END_PATTERN.matcher(line).matches()) scope++;
            else if (CLOSE_CURLY_PATTERN.matcher(line).matches()) scope--;
            if (scope==0) {
                boolean return_at_end = RETURN_PATTERN.matcher(method.get(method.size()-1)).matches();
                if (!return_at_end) throw CompileException.methodDoesntEnd();
                methodsList.put(methodName, method);
                methodsParameters.put(methodName, paramList);
                return;
            }
            method.add(line);
        }
        throw CompileException.methodDoesntEnd(); // reached end of file without closing the method
    }

    private ArrayList<VarType> parseParamList(String paramsList, String methodName)
            throws IllegalSymbolException {
        ArrayList<VarType> params = new ArrayList<>();
        symbolTable.enterScope(); // this both allows us to save params in method definition,
        if (paramsList==null) {
            methodStartingScopes.put(methodName, symbolTable.getLocalSnapshot());
            symbolTable.exitScope();
            return params;
        }
        boolean saveParameters = !(methodStartingScopes.containsKey(methodName));
        Matcher parameterFinder = PARAMETER_PATTERN.matcher(paramsList);
        while (parameterFinder.find()) {
            VarType finality = VarType.NOT_FINAL;
            if (parameterFinder.group(1)!=null) finality = VarType.FINAL;
            VarType paramType = VarType.stringTypeToVarType(parameterFinder.group(SECOND_GROUP));
            params.add(paramType);
            String paramName = parameterFinder.group(THIRD_GROUP);
            if (saveParameters) symbolTable.declareParameter(paramName, finality, paramType);
        }
        if (saveParameters) {
            SymbolTable.Snapshot param_scope = symbolTable.getLocalSnapshot();
            methodStartingScopes.put(methodName, param_scope);
        }
        symbolTable.exitScope();
        return params;
    }

    private void parseMethod(List<String> method) throws CompileException {
        for (String line : method) {
            curLineNum++;
            Matcher methodCallMatcher = METHOD_CALL_PATTERN.matcher(line);
            Matcher declarationMatcher = DECLARE_LINE_PATTERN.matcher(line);
            Matcher assignmentMatcher = ASSIGN_LINE_PATTERN.matcher(line);
            Matcher flowMatcher = FLOW_KEYWORD_PATTERN.matcher(line);
            if (line.isEmpty() || RETURN_PATTERN.matcher(line).matches()) continue;
//            if matches method call: get passed argument list, then parseMethodCall (checking method exists)
            else if (methodCallMatcher.matches()) {
                String calledMethodName = methodCallMatcher.group(1);
                String arguments = methodCallMatcher.group(SECOND_GROUP);
                parseMethodCall(calledMethodName, arguments.strip());
            }
//            if matches declaration/assignment line: parseGlobalStatement(line, lineNumber)
            else if (declarationMatcher.matches() || assignmentMatcher.matches())  parseVarStatement(line);
//            if matches if/while statement: parse condition - iterate through things separated by || and &&
//              and make sure all can be cast to boolean. If yes, then enter scope
            else if (flowMatcher.matches()) {
                Matcher conditionFinder = VALUE_PATTERN.matcher(line);
                conditionFinder.find(); // skip over "while/if" token, which is a match for a var name
                while (conditionFinder.find()) {
                    String condition = conditionFinder.group();
                    VarType conditionType;
                    conditionType = getVarTypeFromValue(condition);
                    VarType.checkLegalAssignment(VarType.BOOLEAN, conditionType);
                }
                symbolTable.enterScope();
            }
//            if matches "}" - exit scope (already verified scopes are legal in copyMethod)
            else if (CLOSE_CURLY_PATTERN.matcher(line).matches()) symbolTable.exitScope();
            else throw CompileException.invalidStatement();
        }
    }

    private VarType getVarTypeFromValue(String value) throws IllegalSymbolException {
        VarType conditionType;
        try {
            conditionType = VarType.valueToVarType(value);
        }
        catch (IllegalSymbolException e) {
            conditionType = symbolTable.getVariableTypeIfAssigned(value);
        }
        return conditionType;
    }

    private void parseMethodCall(String methodName, String arguments)
            throws CompileException {
        ArrayList<VarType> paramList = methodsParameters.get(methodName);
        if (paramList==null) throw CompileException.methodDoesNotExist(methodName);
        ArrayList<VarType> argList = parseArgList(arguments);
        int numArgs = argList.size();
        if (paramList.size()!= numArgs) throw CompileException.wrongParameterCount(paramList.size(),numArgs);
        for (int i=0; i< argList.size(); i++) {
            VarType.checkLegalAssignment(paramList.get(i), argList.get(i));
        }
    }
    private ArrayList<VarType> parseArgList(String arguments) throws IllegalSymbolException {
        ArrayList<VarType> argList = new ArrayList<>();
        Matcher m = VALUE_PATTERN.matcher(arguments);
        while (m.find()) {
            String value = m.group();
            VarType type = getVarTypeFromValue(value);
            argList.add(type);
        }
        return argList;
    }
}
