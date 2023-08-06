# Kaiju

Kaiju is a framework for data analaysis applications. A Kaiju
application contains a set of operations, which correspond to Python
methods in your code. Kaiju offers three main features:

  - Automatic command-line parsing configuration.
  - Logging of operation executions.
  - MongoDB interfacing.

This simplifies your research work by automatically documenting your
analyses and storing their results, making it easy for you to document
and reproduce your work. Kaiju also stimulates you to work from the
system shell instead of from within Python, so your application is a
stand-alone program from the moment you start building it, and not
just a Python module that you are always struggling to integrate to
another system.

## Usage

Create a kaiju.Kaiju object with the desired configuration, and
use the `__call__` to decorate your operation methods.

Kaiju depends on `pymongo` for interacting with MongoDB.

## Kaiju axioms

A Kaiju application is defined by a Kaiju object, an instance from the
Kaiju class.

A Kaiju application contains a set of operations.

Each Kaiju operation is a method from your Python code that was
decorated by the Kaiju object.

These operations can consume and produce data. The consumed data are
the method arguments, and the output data is whatever the method
returns. Operations typically output lists, or generators, and Kaiju
iterates over this output.

The output from a non-logged operation is simply sent to stdout.

The output from a logged operation is stored in MongoDB, in the
collection specified by the decorator argument `output`. Each element
from this output becomes a separate record in the collection.

A logged operation outputs a `maker_id` code, which is the
`_id` assigned to this operation execution in the Kaiju log.

You can specify different types for the operation inputs using the
classes from the kaiju.arguments submodule.

The `Data` input class lets you fetch data from the database. The
argument receives a `maker_id` and outputs to the underlying operation
method a generator for corresponding data.
