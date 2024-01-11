//===- toyc.cpp - The Toy Compiler ----------------------------------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file implements the entry point for the Toy compiler.
//
//===----------------------------------------------------------------------===//
#include <iostream>

#include "toy/Parser.h"

#include "llvm/ADT/StringRef.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/ErrorOr.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/raw_ostream.h"

//Added by ABhinav
#include <iostream>
#include <typeinfo>
//end 


using namespace std;
using namespace toy;
namespace cl = llvm::cl;

//Added by ABhinav
template <typename T> std::string type_name();
//end


static cl::opt<std::string> inputFilename(cl::Positional,
                                          cl::desc("<input toy file>"),
                                          cl::init("-"),
                                          cl::value_desc("filename"));
namespace {
enum Action { None, DumpAST , CustomAbhinav};
} // namespace

static cl::opt<enum Action>
    emitAction("emit", cl::desc("Select the kind of output desired"),
               cl::values(clEnumValN(DumpAST, "ast", "output the AST dump")),
               cl::values(clEnumValN(CustomAbhinav, "abhi", "Just a custom print")));

/// Returns a Toy AST resulting from parsing the file or a nullptr on error.
std::unique_ptr<toy::ModuleAST> parseInputFile(llvm::StringRef filename) {
  llvm::ErrorOr<std::unique_ptr<llvm::MemoryBuffer>> fileOrErr =
      llvm::MemoryBuffer::getFileOrSTDIN(filename);
  if (std::error_code ec = fileOrErr.getError()) {
    llvm::errs() << "Could not open input file: " << ec.message() << "\n";
    return nullptr;
  }
  auto buffer = fileOrErr.get()->getBuffer();
  // llvm::errs() << "type of buffer " << typeid(buffer).name() << "\n";
  // llvm::errs() << "type of buffer " << type_name<decltype(buffer)>() << "\n";
  LexerBuffer lexer(buffer.begin(), buffer.end(), std::string(filename));
  Parser parser(lexer);
  return parser.parseModule();
}

int main(int argc, char **argv) {
  cl::ParseCommandLineOptions(argc, argv, "toy compiler\n");

  auto moduleAST = parseInputFile(inputFilename);
  // cout << "moduleAST -type" << typeid(moduleAST).name() << endl;

  if (!moduleAST)
    return 1;

  switch (emitAction) {
  case Action::DumpAST:
    dump(*moduleAST);
    return 0;
  
  case Action::CustomAbhinav:
      cout << "Just A custom print -- Print1\n";
      break;
      
  default:
    llvm::errs() << "No action specified (parsing only?), use -emit=<action>\n";
  }

  return 0;
}
