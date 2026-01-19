import 'package:fpdart/fpdart.dart';
import 'package:flutter_python/appCore/failure.dart';

typedef FutureEither<T> = Future<Either<Failure, T>>;
typedef FutureVoid = FutureEither<void>;
