---
name: cpp-testing
description: C++ testing strategies using GoogleTest/GoogleMock, TDD workflow, CMake/CTest, coverage, sanitizers, and practical testing patterns.
---

# C++ Testing Patterns

Actionable, example-driven testing guidance for modern C++ (C++17/20) using GoogleTest/GoogleMock, CMake, and CTest.

## When to Activate

- Writing new C++ features or refactoring existing code
- Designing unit and integration tests for libraries or services
- Adding test coverage, CI gating, or regression protection
- Setting up CMake/CTest workflows for consistent test execution

## TDD Workflow for C++

### The Red-Green-Refactor Loop

1. **RED**: Write a failing test for the new behavior
2. **GREEN**: Implement the minimal code to pass
3. **REFACTOR**: Improve the design while keeping tests green

```cpp
// calculator_test.cpp
#include <gtest/gtest.h>

int Add(int a, int b); // Step 1: declare the behavior

TEST(CalculatorTest, AddsTwoNumbers) { // Step 1: RED
    EXPECT_EQ(Add(2, 3), 5);
}

// calculator.cpp
int Add(int a, int b) { // Step 2: GREEN
    return a + b;
}

// Step 3: REFACTOR when needed, keeping tests green
```

## Core Patterns

### Basic Test Structure

```cpp
#include <gtest/gtest.h>

int Clamp(int value, int lo, int hi);

TEST(ClampTest, ReturnsLowerBound) {
    EXPECT_EQ(Clamp(-1, 0, 10), 0);
}

TEST(ClampTest, ReturnsUpperBound) {
    EXPECT_EQ(Clamp(42, 0, 10), 10);
}

TEST(ClampTest, ReturnsValueInRange) {
    EXPECT_EQ(Clamp(5, 0, 10), 5);
}
```

### Fixtures for Shared Setup

```cpp
#include <gtest/gtest.h>
#include "user_store.h"

class UserStoreTest : public ::testing::Test {
protected:
    void SetUp() override {
        store = std::make_unique<UserStore>(":memory:");
        store->Seed({{"alice"}, {"bob"}});
    }

    std::unique_ptr<UserStore> store;
};

TEST_F(UserStoreTest, FindsExistingUser) {
    auto user = store->Find("alice");
    ASSERT_TRUE(user.has_value());
    EXPECT_EQ(user->name, "alice");
}
```

### Parameterized Tests

```cpp
#include <gtest/gtest.h>

struct Case {
    int input;
    int expected;
};

class AbsTest : public ::testing::TestWithParam<Case> {};

TEST_P(AbsTest, HandlesValues) {
    auto [input, expected] = GetParam();
    EXPECT_EQ(std::abs(input), expected);
}

INSTANTIATE_TEST_SUITE_P(
    BasicCases,
    AbsTest,
    ::testing::Values(
        Case{-3, 3},
        Case{0, 0},
        Case{7, 7}
    )
);
```

### Death Tests (Failure Conditions)

```cpp
#include <gtest/gtest.h>

void RequirePositive(int value) {
    if (value <= 0) {
        std::abort();
    }
}

TEST(DeathTest, AbortsOnNonPositive) {
    ASSERT_DEATH(RequirePositive(0), "");
}
```

### GoogleMock for Behavior Verification

```cpp
#include <gmock/gmock.h>
#include <gtest/gtest.h>

class Notifier {
public:
    virtual ~Notifier() = default;
    virtual void Send(const std::string &message) = 0;
};

class MockNotifier : public Notifier {
public:
    MOCK_METHOD(void, Send, (const std::string &message), (override));
};

class Service {
public:
    explicit Service(Notifier &notifier) : notifier_(notifier) {}
    void Publish(const std::string &message) {
        notifier_.Send(message);
    }

private:
    Notifier &notifier_;
};

TEST(ServiceTest, SendsNotifications) {
    MockNotifier notifier;
    Service service(notifier);

    EXPECT_CALL(notifier, Send("hello"))
        .Times(1);

    service.Publish("hello");
}
```

### Fakes vs Mocks

- **Fake**: a lightweight in-memory implementation to exercise logic (great for stateful systems)
- **Mock**: used to assert interactions or order of operations

Prefer fakes for higher signal tests, use mocks only when behavior is the real contract.

## Test Organization

Recommended structure:

```
project/
|-- CMakeLists.txt
|-- include/
|-- src/
|-- tests/
|   |-- unit/
|   |-- integration/
|   |-- testdata/
```

Keep unit tests close to the source, keep integration tests in their own folders, and isolate large fixtures in `testdata/`.

## CMake + CTest Workflow

### FetchContent for GoogleTest/GoogleMock

```cmake
cmake_minimum_required(VERSION 3.20)
project(example LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
FetchContent_MakeAvailable(googletest)

add_executable(example_tests
  tests/calculator_test.cpp
  src/calculator.cpp
)

target_link_libraries(example_tests
  GTest::gtest
  GTest::gmock
  GTest::gtest_main
)

enable_testing()
include(GoogleTest)
gtest_discover_tests(example_tests)
```

### Configure, Build, Run

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build -j
ctest --test-dir build --output-on-failure
```

### Run a Subset of Tests

```bash
ctest --test-dir build -R ClampTest
ctest --test-dir build -R "UserStoreTest.*" --output-on-failure
```

## Coverage Workflows

### GCC + gcov + lcov

```bash
cmake -S . -B build-cov -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_CXX_FLAGS="--coverage"
cmake --build build-cov -j
ctest --test-dir build-cov

lcov --capture --directory build-cov --output-file coverage.info
lcov --remove coverage.info '/usr/*' --output-file coverage.info

genhtml coverage.info --output-directory coverage
```

### LLVM/Clang + llvm-cov

```bash
cmake -S . -B build-llvm -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_CXX_COMPILER=clang++ \
  -DCMAKE_CXX_FLAGS="-fprofile-instr-generate -fcoverage-mapping"
cmake --build build-llvm -j

LLVM_PROFILE_FILE="build-llvm/default.profraw" \
ctest --test-dir build-llvm

llvm-profdata merge -sparse build-llvm/default.profraw -o build-llvm/default.profdata
llvm-cov report build-llvm/example_tests \
  -instr-profile=build-llvm/default.profdata
```

## Sanitizers

### Common Flags

- AddressSanitizer (ASan): `-fsanitize=address`
- UndefinedBehaviorSanitizer (UBSan): `-fsanitize=undefined`
- ThreadSanitizer (TSan): `-fsanitize=thread`

### CMake Toggle Example

```cmake
option(ENABLE_ASAN "Enable AddressSanitizer" OFF)
option(ENABLE_UBSAN "Enable UndefinedBehaviorSanitizer" OFF)
option(ENABLE_TSAN "Enable ThreadSanitizer" OFF)

if(ENABLE_ASAN)
  add_compile_options(-fsanitize=address -fno-omit-frame-pointer)
  add_link_options(-fsanitize=address)
endif()

if(ENABLE_UBSAN)
  add_compile_options(-fsanitize=undefined -fno-omit-frame-pointer)
  add_link_options(-fsanitize=undefined)
endif()

if(ENABLE_TSAN)
  add_compile_options(-fsanitize=thread)
  add_link_options(-fsanitize=thread)
endif()
```

Usage:

```bash
cmake -S . -B build-asan -DENABLE_ASAN=ON
cmake --build build-asan
ctest --test-dir build-asan --output-on-failure
```

## Common Scenarios

### API-Like Boundaries (Interfaces)

```cpp
class Clock {
public:
    virtual ~Clock() = default;
    virtual std::chrono::system_clock::time_point Now() const = 0;
};

class SystemClock : public Clock {
public:
    std::chrono::system_clock::time_point Now() const override {
        return std::chrono::system_clock::now();
    }
};

class Session {
public:
    Session(Clock &clock, std::chrono::seconds ttl)
        : clock_(clock), ttl_(ttl) {}

    bool IsExpired(std::chrono::system_clock::time_point created) const {
        return (clock_.Now() - created) > ttl_;
    }

private:
    Clock &clock_;
    std::chrono::seconds ttl_;
};
```

### Filesystem Isolation

```cpp
#include <filesystem>
#include <gtest/gtest.h>

TEST(FileTest, WritesOutput) {
    auto temp = std::filesystem::temp_directory_path() / "cpp-testing";
    std::filesystem::create_directories(temp);

    auto file = temp / "output.txt";
    std::ofstream out(file);
    out << "hello";
    out.close();

    std::ifstream in(file);
    std::string content;
    in >> content;

    EXPECT_EQ(content, "hello");

    std::filesystem::remove_all(temp);
}
```

### Time-Dependent Logic

```cpp
class FakeClock : public Clock {
public:
    explicit FakeClock(std::chrono::system_clock::time_point now) : now_(now) {}
    std::chrono::system_clock::time_point Now() const override { return now_; }
    void Advance(std::chrono::seconds delta) { now_ += delta; }

private:
    std::chrono::system_clock::time_point now_;
};
```

### Concurrency (Deterministic Tests)

```cpp
#include <condition_variable>
#include <mutex>
#include <thread>

TEST(WorkerTest, SignalsCompletion) {
    std::mutex mu;
    std::condition_variable cv;
    bool done = false;

    std::thread worker([&] {
        std::lock_guard<std::mutex> lock(mu);
        done = true;
        cv.notify_one();
    });

    std::unique_lock<std::mutex> lock(mu);
    bool ok = cv.wait_for(lock, std::chrono::milliseconds(500), [&] { return done; });

    worker.join();
    ASSERT_TRUE(ok);
}
```

## Best Practices

### DO

- Keep tests deterministic and isolated
- Prefer dependency injection over globals
- Use `ASSERT_*` for preconditions, `EXPECT_*` for multiple checks
- Separate unit vs integration tests in CTest labels or directories
- Run sanitizers in CI for memory and race detection

### DON'T

- Don't depend on real time or network in unit tests
- Don't use sleeps as synchronization when a condition variable can be used
- Don't over-mock simple value objects
- Don't use brittle string matching for non-critical logs

## Alternatives to GoogleTest

- **Catch2**: header-only, expressive matchers, fast setup
- **doctest**: lightweight, minimal compile overhead

## Fuzzing and Property Testing

- **libFuzzer**: integrate with LLVM; focus on pure functions with minimal I/O
- **RapidCheck**: property-based testing to validate invariants over many inputs

Minimal libFuzzer harness:

```cpp
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    std::string input(reinterpret_cast<const char *>(data), size);
    ParseConfig(input);
    return 0;
}
```
