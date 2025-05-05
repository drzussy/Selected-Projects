---

# Checker – Semantic Checker & Symbol Management for s-Java

This package implements a semantic checker for the s-Java language. It provides scoped variable tracking, type enforcement, assignment rules, and error reporting for compilation.
Refer to my_tests file for examples of valid and invalid code that ou may run through the compiler.
Refer to the uml of the project for full api and structure.
---

## Components Overview

### SymbolTable

Central class for managing declared variables and their scope.

* **Variable Declaration**: Declares variables with type, finality, and assignment state.
* **Assignment**: Assigns values to variables, checking type compatibility and finality.
* **Scoping**:

  * `enterScope()` / `exitScope()` handle nested blocks.
  * Variables follow lexical scoping and shadowing rules.
* **Snapshot System**:

  * `getGlobalSnapshot()` / `restoreGlobalSnapshot(...)`
  * `getLocalSnapshot()` / `restoreLocalSnapshot(...)`
  * Useful for temporary analysis (e.g., method pre-checks).
* **Parameter Declaration**: Declared as assigned by default.

Each variable is stored as a `Map<String, VarType>` with:

* `"isFinal"`: `FINAL` or `NOT_FINAL`
* `"type"`: one of `INT`, `DOUBLE`, `CHAR`, `STRING`, `BOOLEAN`
* `"isAssigned"`: `ASSIGNED` or `UNASSIGNED`

---

### VarType (enum)

Represents primitive types, assignment states, and finality. Includes:

* `INT`, `DOUBLE`, `CHAR`, `STRING`, `BOOLEAN`
* `ASSIGNED`, `UNASSIGNED`
* `FINAL`, `NOT_FINAL`

#### Methods:

* `stringTypeToVarType(String)` – Converts `"int"` to `VarType.INT`.
* `valueToVarType(String)` – Infers type from value string (`"5" → INT`).
* `checkLegalAssignment(receiver, giver)` – Allows valid type promotions:

  * Valid: `int → double`, `int → boolean`, `double → boolean`
  * Invalid: all other cross-type assignments

---

### CompileException

Base exception for compile-time errors.

Static constructors for common errors:

* `methodDoesntEnd()`
* `doubleMethodDeclaration(name)`
* `invalidVarType()`
* `noVarNameFound()`
* `illegalComment()`
* `invalidStatement()`
* `invalidMethodDeclaration()`
* `methodDoesNotExist(name)`
* `wrongParameterCount(shouldBe, passed)`

---

### IllegalSymbolException

Subclass of `CompileException`, thrown on illegal symbol operations.

Covers:

* Undefined variable: `symbolNotFound(name)`
* Unassigned usage: `unassignedUsage(name)`
* Re-declaration: `varAlreadyExists(name)`
* Assignment to `final`: `assignmentToFinalVar(name)`
* Type mismatch: `illegalAssignment(receiver, giver)`
* Final declared without initialization: `uninitializedFinalVar(name)`
* Reserved variable name: `illegalVarName(name)`
* Snapshot misuse:

  * No current local scope: `noLocalTableFound()`
  * Null snapshot: `noSnapshotGiven()`

---

## Example

```java
symbolTable.enterScope();
symbolTable.declareVar("x", VarType.NOT_FINAL, VarType.INT);
symbolTable.assignToVar("x", VarType.INT);
VarType xType = symbolTable.getVariableTypeIfAssigned("x"); // INT
symbolTable.exitScope();
```

---

## Notes

* Reserved names like `"true"`/`"false"` are not allowed as variable identifiers.
* Final variables must be initialized immediately.
* Scope stack ensures variable shadowing is handled correctly.
* Exceptions are designed to be descriptive and recoverable.

---
