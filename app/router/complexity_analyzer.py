from dataclasses import dataclass
from typing import Literal


ComplexityLevel = Literal[
    "low",
    "medium",
    "high",
]


@dataclass(frozen=True)
class ComplexityResult:
    """
    Final result produced by the complexity analyzer.
    """

    level: ComplexityLevel
    score: int
    features: dict[str, int | float]
    reasons: list[str]


class ComplexityAnalyzer:
    """
    Rule-based baseline complexity analyzer.

    The analyzer extracts multiple independent features
    from a prompt and combines them into a heuristic score.

    This is intentionally deterministic. Later, the same
    features can be used to train an ML classifier.
    """

    # --------------------------------------------------
    # Technical concepts
    # --------------------------------------------------

    TECHNICAL_TERMS = {
        "python",
        "java",
        "javascript",
        "typescript",
        "django",
        "fastapi",
        "flask",
        "react",
        "node",
        "sql",
        "postgresql",
        "mysql",
        "mongodb",
        "redis",
        "kafka",
        "api",
        "rest",
        "graphql",
        "docker",
        "kubernetes",
        "aws",
        "algorithm",
        "database",
        "backend",
        "frontend",
        "machine learning",
        "deep learning",
        "llm",
        "rag",
        "langchain",
        "langgraph",
        "microservices",
    }

    # --------------------------------------------------
    # Reasoning
    # --------------------------------------------------

    REASONING_TERMS = {
        "why",
        "explain",
        "compare",
        "analyze",
        "analyse",
        "reason",
        "justify",
        "evaluate",
        "trade-off",
        "tradeoff",
        "pros and cons",
    }

    # --------------------------------------------------
    # System design
    # --------------------------------------------------

    SYSTEM_DESIGN_TERMS = {
        "architecture",
        "architect",
        "system design",
        "distributed",
        "scalable",
        "scalability",
        "microservices",
        "service architecture",
        "high availability",
        "fault tolerant",
        "fault-tolerant",
    }

    # --------------------------------------------------
    # Reliability / distributed-system complexity
    # --------------------------------------------------

    RELIABILITY_TERMS = {
        "fault tolerance",
        "fault-tolerant",
        "failure recovery",
        "retry",
        "retries",
        "idempotency",
        "consistency",
        "data consistency",
        "high availability",
        "availability",
        "replication",
        "failover",
        "recovery",
    }

    # --------------------------------------------------
    # Performance
    # --------------------------------------------------

    PERFORMANCE_TERMS = {
        "optimization",
        "optimize",
        "performance",
        "latency",
        "throughput",
        "scalability",
        "memory",
        "time complexity",
        "space complexity",
    }

    # --------------------------------------------------
    # Implementation / complex task
    # --------------------------------------------------

    IMPLEMENTATION_TERMS = {
        "implement",
        "build",
        "develop",
        "create",
        "integrate",
        "refactor",
        "debug",
        "debugging",
        "fix",
    }

    # --------------------------------------------------
    # Constraints
    # --------------------------------------------------

    CONSTRAINT_TERMS = {
        "without",
        "must",
        "should",
        "constraint",
        "constraints",
        "limit",
        "limited",
        "under",
        "within",
        "maximum",
        "minimum",
        "at least",
        "at most",
        "no more than",
        "only",
        "required",
        "requirement",
        "requirements",
    }

    # --------------------------------------------------
    # Output requirements
    # --------------------------------------------------

    OUTPUT_TERMS = {
        "code",
        "implementation",
        "example",
        "examples",
        "steps",
        "step by step",
        "test",
        "tests",
        "documentation",
        "report",
        "table",
        "architecture diagram",
        "explain",
    }

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def analyze(
        self,
        prompt: str,
    ) -> ComplexityResult:
        """
        Analyze a prompt and return its estimated complexity.
        """

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        prompt = prompt.strip()
        normalized_prompt = prompt.lower()

        features = self._extract_features(
            prompt=prompt,
            normalized_prompt=normalized_prompt,
        )

        score, reasons = self._calculate_score(
            features
        )

        level = self._classify_score(
            score
        )

        return ComplexityResult(
            level=level,
            score=score,
            features=features,
            reasons=reasons,
        )

    # ==================================================
    # Feature Extraction
    # ==================================================

    def _extract_features(
        self,
        prompt: str,
        normalized_prompt: str,
    ) -> dict[str, int | float]:

        words = prompt.split()

        word_count = len(words)

        sentence_count = self._count_sentences(
            prompt
        )

        question_count = prompt.count("?")

        technical_matches = self._find_matches(
            normalized_prompt,
            self.TECHNICAL_TERMS,
        )

        reasoning_matches = self._find_matches(
            normalized_prompt,
            self.REASONING_TERMS,
        )

        system_design_matches = self._find_matches(
            normalized_prompt,
            self.SYSTEM_DESIGN_TERMS,
        )

        reliability_matches = self._find_matches(
            normalized_prompt,
            self.RELIABILITY_TERMS,
        )

        performance_matches = self._find_matches(
            normalized_prompt,
            self.PERFORMANCE_TERMS,
        )

        implementation_matches = self._find_matches(
            normalized_prompt,
            self.IMPLEMENTATION_TERMS,
        )

        constraint_matches = self._find_matches(
            normalized_prompt,
            self.CONSTRAINT_TERMS,
        )

        output_matches = self._find_matches(
            normalized_prompt,
            self.OUTPUT_TERMS,
        )

        instruction_count = self._count_instructions(
            normalized_prompt
        )

        step_count = self._count_step_indicators(
            normalized_prompt
        )

        numeric_constraint_count = (
            self._count_numeric_constraints(
                normalized_prompt
            )
        )

        return {
            # Basic prompt structure
            "word_count": word_count,
            "sentence_count": sentence_count,
            "question_count": question_count,

            # Domain / technical complexity
            "technical_depth": len(
                technical_matches
            ),

            # Reasoning
            "reasoning": len(
                reasoning_matches
            ),

            # System design
            "system_design": len(
                system_design_matches
            ),

            # Reliability
            "reliability": len(
                reliability_matches
            ),

            # Performance
            "performance": len(
                performance_matches
            ),

            # Implementation
            "implementation": len(
                implementation_matches
            ),

            # Constraints
            "constraints": len(
                constraint_matches
            ),

            "numeric_constraints": (
                numeric_constraint_count
            ),

            # Multi-step
            "instruction_count": instruction_count,
            "step_count": step_count,

            # Output complexity
            "output_requirements": len(
                output_matches
            ),
        }

    # ==================================================
    # Heuristic Scoring
    # ==================================================

    def _calculate_score(
        self,
        features: dict[str, int | float],
    ) -> tuple[int, list[str]]:

        score = 0
        reasons: list[str] = []

        # ----------------------------------------------
        # 1. Prompt length
        # ----------------------------------------------

        word_count = int(
            features["word_count"]
        )

        if word_count > 150:
            score += 3
            reasons.append(
                "Very long prompt"
            )

        elif word_count > 75:
            score += 2
            reasons.append(
                "Long prompt"
            )

        elif word_count > 40:
            score += 1
            reasons.append(
                "Moderately long prompt"
            )

        # ----------------------------------------------
        # 2. Technical depth
        # ----------------------------------------------

        technical_depth = int(
            features["technical_depth"]
        )

        if technical_depth >= 6:
            score += 4
            reasons.append(
                "High technical depth"
            )

        elif technical_depth >= 3:
            score += 2
            reasons.append(
                "Several technical concepts"
            )

        elif technical_depth >= 1:
            score += 1
            reasons.append(
                "Technical concept detected"
            )

        # ----------------------------------------------
        # 3. Reasoning
        # ----------------------------------------------

        reasoning = int(
            features["reasoning"]
        )

        if reasoning >= 3:
            score += 3
            reasons.append(
                "Strong reasoning requirement"
            )

        elif reasoning >= 1:
            score += 2
            reasons.append(
                "Requires explanation or reasoning"
            )

        # ----------------------------------------------
        # 4. System design
        # ----------------------------------------------

        system_design = int(
            features["system_design"]
        )

        if system_design >= 4:
            score += 5
            reasons.append(
                "Strong system-design complexity"
            )

        elif system_design >= 2:
            score += 3
            reasons.append(
                "System-design concepts detected"
            )

        elif system_design >= 1:
            score += 2
            reasons.append(
                "System-design requirement detected"
            )

        # ----------------------------------------------
        # 5. Reliability
        # ----------------------------------------------

        reliability = int(
            features["reliability"]
        )

        if reliability >= 4:
            score += 5
            reasons.append(
                "Multiple reliability or "
                "failure-handling requirements"
            )

        elif reliability >= 2:
            score += 3
            reasons.append(
                "Reliability requirements detected"
            )

        elif reliability >= 1:
            score += 2
            reasons.append(
                "Reliability requirement detected"
            )

        # ----------------------------------------------
        # 6. Performance
        # ----------------------------------------------

        performance = int(
            features["performance"]
        )

        if performance >= 4:
            score += 3
            reasons.append(
                "Strong performance requirements"
            )

        elif performance >= 2:
            score += 2
            reasons.append(
                "Performance considerations detected"
            )

        elif performance >= 1:
            score += 1
            reasons.append(
                "Performance consideration detected"
            )

        # ----------------------------------------------
        # 7. Implementation complexity
        # ----------------------------------------------

        implementation = int(
            features["implementation"]
        )

        if implementation >= 3:
            score += 3
            reasons.append(
                "Multiple implementation requirements"
            )

        elif implementation >= 1:
            score += 1
            reasons.append(
                "Implementation work requested"
            )

        # ----------------------------------------------
        # 8. Constraints
        # ----------------------------------------------

        constraints = int(
            features["constraints"]
        )

        if constraints >= 4:
            score += 3
            reasons.append(
                "Multiple constraints"
            )

        elif constraints >= 2:
            score += 2
            reasons.append(
                "Several constraints"
            )

        elif constraints >= 1:
            score += 1
            reasons.append(
                "Constraint detected"
            )

        # Quantitative constraints get additional weight.
        numeric_constraints = int(
            features["numeric_constraints"]
        )

        if numeric_constraints >= 2:
            score += 2
            reasons.append(
                "Multiple quantitative constraints"
            )

        elif numeric_constraints == 1:
            score += 1
            reasons.append(
                "Quantitative constraint detected"
            )

        # ----------------------------------------------
        # 9. Multi-step requirements
        # ----------------------------------------------

        instruction_count = int(
            features["instruction_count"]
        )

        step_count = int(
            features["step_count"]
        )

        if (
            instruction_count >= 4
            or step_count >= 3
        ):
            score += 3
            reasons.append(
                "Multiple steps or instructions"
            )

        elif (
            instruction_count >= 2
            or step_count >= 1
        ):
            score += 2
            reasons.append(
                "Multi-step task"
            )

        # ----------------------------------------------
        # 10. Output complexity
        # ----------------------------------------------

        output_requirements = int(
            features["output_requirements"]
        )

        if output_requirements >= 5:
            score += 3
            reasons.append(
                "Multiple output requirements"
            )

        elif output_requirements >= 3:
            score += 2
            reasons.append(
                "Structured output requested"
            )

        elif output_requirements >= 1:
            score += 1
            reasons.append(
                "Specific output requested"
            )

        return score, reasons

    # ==================================================
    # Classification
    # ==================================================

    @staticmethod
    def _classify_score(
        score: int,
    ) -> ComplexityLevel:

        if score <= 4:
            return "low"

        if score <= 9:
            return "medium"

        return "high"

    # ==================================================
    # Helper Methods
    # ==================================================

    @staticmethod
    def _find_matches(
        text: str,
        patterns: set[str],
    ) -> list[str]:
        """
        Find vocabulary patterns appearing in the prompt.

        Each pattern is counted at most once.
        """

        return [
            pattern
            for pattern in patterns
            if pattern in text
        ]

    @staticmethod
    def _count_sentences(
        text: str,
    ) -> int:

        count = (
            text.count(".")
            + text.count("!")
            + text.count("?")
        )

        return max(
            count,
            1,
        )

    @staticmethod
    def _count_instructions(
        text: str,
    ) -> int:

        instruction_patterns = {
            "explain",
            "describe",
            "compare",
            "analyze",
            "analyse",
            "design",
            "build",
            "create",
            "implement",
            "write",
            "provide",
            "calculate",
            "find",
            "debug",
            "fix",
            "optimize",
            "optimise",
            "list",
        }

        return sum(
            1
            for pattern in instruction_patterns
            if pattern in text
        )

    @staticmethod
    def _count_step_indicators(
        text: str,
    ) -> int:

        indicators = {
            "step 1",
            "step 2",
            "step 3",
            "first",
            "second",
            "third",
            "then",
            "after that",
            "finally",
        }

        return sum(
            1
            for indicator in indicators
            if indicator in text
        )

    @staticmethod
    def _count_numeric_constraints(
        text: str,
    ) -> int:

        numeric_patterns = {
            "ms",
            "seconds",
            "second",
            "minutes",
            "minute",
            "kb",
            "mb",
            "gb",
            "%",
            "o(",
            "n <",
            "n >",
            "under ",
            "within ",
            "at least ",
            "at most ",
            "maximum ",
            "minimum ",
        }

        return sum(
            1
            for pattern in numeric_patterns
            if pattern in text
        )