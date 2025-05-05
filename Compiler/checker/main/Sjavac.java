package checker.main;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.regex.Pattern;

import checker.*;

/**
 * The Sjavac class provides functionality to validate `.sjava` files for syntax correctness.
 * It processes the provided file, checks for valid syntax, and outputs a specific status code:
 * <ul>
 *   <li><code>0</code>: The s-java code is legal.</li>
 *   <li><code>1</code>: The s-java code is illegal.</li>
 *   <li><code>2</code>: An I/O error occurred during file processing.</li>
 * </ul>
 * <p>
 * The class uses a {@code Parser} instance to analyze the file,
 * and reports detailed errors when exceptions are thrown.
 */
public class Sjavac {
    private static final int LEGAL_CODE_OUTPUT = 0;
    private static final int ILLEGAL_CODE_OUTPUT = 1;
    private static final int IOEXCEPTION_OUTPUT = 2;
    private static final String GENERAL_IO_ERROR_MESSAGE = "Error while reading the file!";
    private static final String WRONG_PARAMETER_COUNT_MESSAGE = "Wrong number of arguments in cml!";
    private static final Pattern EXTENSION_PATTERN = Pattern.compile(".*\\.sjava$");
    private static final String EXTENSION_ERROR = "Wrong file extension!";
    private static final String LINE = " Line ";
    private static final String COLON_SPACE = ": ";


    /**
     * The ex5.main method validates a given `.sjava` file for syntax correctness.
     * Outputs specific status codes based on the file's validity or errors encountered.
     * Status codes:
     * <ul>
     *   <li><code>0</code>: The s-java code is legal.</li>
     *   <li><code>1</code>: The s-java code is illegal.</li>
     *   <li><code>2</code>: An I/O error occurred during file processing.</li>
     * </ul>
     * @param args A string array, which contains only the name of the `.sjava` file to verify.
     */
    public static void main(String[] args) {
        String filename;
        try {
            if(args.length != 1) throw new IOException(WRONG_PARAMETER_COUNT_MESSAGE);
            filename = args[0];
            if (!EXTENSION_PATTERN.matcher(filename).matches()) throw new IOException(EXTENSION_ERROR);
        }
        catch (IOException e) {
            System.out.println(IOEXCEPTION_OUTPUT);
            System.err.println(e.getMessage());
            return;
        }
        Parser parser = new Parser();
        try (FileReader fileReader = new FileReader(filename);
                BufferedReader bufferedReader = new BufferedReader(fileReader)) {
            parser.parseFile(bufferedReader);
            System.out.println(LEGAL_CODE_OUTPUT);
        } catch(IOException e){
            System.err.println(GENERAL_IO_ERROR_MESSAGE);
            System.out.println(IOEXCEPTION_OUTPUT);
        } catch(CompileException e) {
            System.err.println(LINE+parser.getCurrentLine()+COLON_SPACE+e.getMessage());
            System.out.println(ILLEGAL_CODE_OUTPUT);
        }
    }
}
