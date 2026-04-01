# https://skillsmp.com/ko/skills/linguistic76-skuel-app-claude-skills-neo4j-cypher-patterns-skill-md

Pattern 1: MERGE + SET — Idempotent Relationship Creation

Problem: Creating a relationship that may already exist, with metadata you want to update.

Context: Domain backends linking entities (task→knowledge, habit→goal, event→knowledge).

Solution:

// TasksBackend.link_task_to_knowledge()
MATCH (t:Task {uid: $task_uid})
MATCH (k:Entity {uid: $knowledge_uid})
MERGE (t)-[r:REQUIRES_KNOWLEDGE]->(k)
SET r.knowledge_score_required = $knowledge_score_required,
    r.is_learning_opportunity = $is_learning_opportunity
RETURN r

// GoalsBackend.link_task_to_goal()
MATCH (t:Task {uid: $task_uid})
MATCH (g:Goal {uid: $goal_uid})
MERGE (t)-[r:CONTRIBUTES_TO_GOAL]->(g)
SET r.contribution_percentage = $contribution_percentage
RETURN r
Python (via backend):

# domain_backends.py pattern — uses self.execute_query() (inherited from UniversalNeo4jBackend)
async def link_task_to_knowledge(
    self, task_uid: str, knowledge_uid: str,
    knowledge_score_required: float = 0.8,
    is_learning_opportunity: bool = False,
) -> Result[bool]:
    query = """
    MATCH (t:Task {uid: $task_uid})
    MATCH (k:Entity {uid: $knowledge_uid})
    MERGE (t)-[r:REQUIRES_KNOWLEDGE]->(k)
    SET r.knowledge_score_required = $knowledge_score_required,
        r.is_learning_opportunity = $is_learning_opportunity
    RETURN r
    """
    params = {
        "task_uid": task_uid,
        "knowledge_uid": knowledge_uid,
        "knowledge_score_required": knowledge_score_required,
        "is_learning_opportunity": is_learning_opportunity,
    }
    result = await self.execute_query(query, params)
    if result.is_error:
        return Result.fail(result)
    return Result.ok(True)
Trade-offs:

MERGE is idempotent — safe to call multiple times
SET overwrites relationship properties on each call