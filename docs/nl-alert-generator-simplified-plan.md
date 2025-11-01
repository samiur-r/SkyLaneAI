# Natural Language Alert Generator - Simplified Implementation Plan

**Project:** SkyLaneAI v2
**Feature:** Natural Language Alert System
**Version:** 1.0 (Simplified)
**Date:** 2025-11-01
**Technologies:** LangGraph, OpenAI GPT-4o-mini

---

## Overview

Transform raw YOLOv11 detection data into human-readable, actionable alerts for flying taxi operators. This simplified version focuses on core alert generation without complex historical analysis or feedback loops.

### Simplified Example

**Input (Raw Detection):**
```json
{
  "class_name": "bird",
  "class_id": 14,
  "confidence": 0.87,
  "bbox": {"x1": 120, "y1": 340, "x2": 180, "y2": 420},
  "frame_number": 1234,
  "timestamp": 41.13
}
```

**Output (Natural Language Alert):**
```
🔴 CRITICAL ALERT

🦅 Large Bird Detection
Detected at 41.1 seconds | Upper-right quadrant | 87% confidence

📊 Threat Assessment:
• Size: Large (estimated 2-3 kg based on detection area)
• Position: Upper-right quadrant
• Confidence Level: High (87%)

⚠️ RECOMMENDED ACTION:
• IMMEDIATE: Reduce altitude by 50 feet
• Maintain current speed
• Monitor right-side camera for confirmation

Priority: HIGH
```

---

## Simplified Architecture

### System Flow

```
┌─────────────────┐
│   YOLOv11       │
│   Detection     │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Alert Generator Service (FastAPI)      │
│                                          │
│  ┌────────────────────────────────────┐ │
│  │   LangGraph Workflow               │ │
│  │                                    │ │
│  │   1. Context Agent                 │ │
│  │      ↓                             │ │
│  │   2. Message Agent                 │ │
│  │      ↓                             │ │
│  │   3. Action Agent                  │ │
│  │      ↓                             │ │
│  │   4. Priority Agent                │ │
│  │                                    │ │
│  └────────────────────────────────────┘ │
│                                          │
│  GPT-4o-mini                            │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Frontend       │
│  Alert Display  │
└─────────────────┘
```

### Agent Workflow (Simplified)

```
Detection Input
    ↓
[Agent 1] Context Enrichment
    • Calculate object size from bbox
    • Determine screen position
    • Estimate basic threat level
    ↓
[Agent 2] Message Crafting
    • Generate human-readable description
    • Format with emojis and structure
    • Create scannable sections
    ↓
[Agent 3] Action Recommendation
    • Provide specific pilot actions
    • Reference SOPs (embedded in prompts)
    • Prioritize by urgency
    ↓
[Agent 4] Priority Scoring
    • Assign severity (Green/Yellow/Orange/Red)
    • Consider confidence, size, position
    • Justify priority level
    ↓
Final Alert Output
```

---

## Technical Design

### Technology Stack

**Backend:**
- **LangGraph**: Agent orchestration
- **OpenAI GPT-4o-mini**: Language model
- **FastAPI**: API endpoint (existing)
- **Pydantic**: Data validation (existing)

**Frontend:**
- **Next.js + React**: Alert display (existing)
- **shadcn/ui**: Alert components (existing)

### Data Models

```python
# Input
class Detection(BaseModel):
    class_name: str
    class_id: int
    confidence: float
    bbox: dict  # {x1, y1, x2, y2}
    frame_number: int
    timestamp: float

# Agent Outputs
class EnrichedContext(BaseModel):
    estimated_size: str  # "small", "medium", "large"
    bbox_area_pixels: int
    screen_position: str  # "upper-left", "center", etc.
    threat_level_raw: str

class CraftedMessage(BaseModel):
    title: str
    emoji: str
    body: str
    sections: dict

class ActionRecommendation(BaseModel):
    immediate_actions: list[str]
    monitoring_actions: list[str]
    contingency_actions: list[str]

class PriorityScore(BaseModel):
    level: str  # "green", "yellow", "orange", "red"
    score: int  # 1-10
    reasoning: str

# Final Output
class NaturalLanguageAlert(BaseModel):
    alert_id: str
    detection: Detection
    message: CraftedMessage
    actions: ActionRecommendation
    priority: PriorityScore
    generated_at: datetime
```

### API Endpoints

```python
# New endpoint in FastAPI
@router.post("/api/v1/alerts/generate", response_model=NaturalLanguageAlert)
async def generate_nl_alert(detection: Detection):
    """Generate natural language alert from detection"""
    pass

# Used by frontend
@router.get("/api/v1/alerts/{alert_id}")
async def get_alert(alert_id: str):
    """Retrieve generated alert"""
    pass
```

---

## Agent Implementation Details

### Agent 1: Context Enrichment

**Purpose:** Extract basic contextual information from detection data.

**Implementation:**
```python
class ContextEnrichmentAgent:
    """Rule-based context extraction - minimal LLM usage"""

    def enrich(self, detection: Detection) -> EnrichedContext:
        # Calculate bbox area
        bbox = detection.bbox
        area = (bbox["x2"] - bbox["x1"]) * (bbox["y2"] - bbox["y1"])

        # Estimate size based on class and area
        size = self._estimate_size(detection.class_name, area)

        # Determine screen position
        position = self._get_screen_position(bbox)

        # Initial threat level
        threat = self._calculate_threat(detection.confidence, size)

        return EnrichedContext(
            estimated_size=size,
            bbox_area_pixels=area,
            screen_position=position,
            threat_level_raw=threat
        )

    def _estimate_size(self, class_name: str, area: int) -> str:
        """Map bbox area to size categories"""
        thresholds = {
            "bird": {"small": 5000, "medium": 15000},
            "drone": {"small": 8000, "medium": 20000},
            "balloon": {"small": 10000, "medium": 25000},
            "kite": {"small": 7000, "medium": 18000}
        }

        if area < thresholds[class_name]["small"]:
            return "small"
        elif area < thresholds[class_name]["medium"]:
            return "medium"
        else:
            return "large"
```

**Cost:** ~$0 (rule-based, no LLM)

---

### Agent 2: Message Crafting

**Purpose:** Generate human-readable alert message.

**Implementation:**
```python
class MessageCraftingAgent:
    """LLM-powered message generation"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

    async def craft_message(
        self,
        detection: Detection,
        context: EnrichedContext
    ) -> CraftedMessage:

        prompt = f"""You are an aviation safety expert communicating to pilots.

Detection:
- Object: {detection.class_name}
- Confidence: {detection.confidence:.0%}
- Size: {context.estimated_size}
- Position: {context.screen_position}
- Time: {detection.timestamp:.1f} seconds

Generate a clear, concise alert message with:
1. Title with appropriate emoji (🦅 bird, 🚁 drone, 🎈 balloon, 🪁 kite)
2. Detection details section
3. Threat assessment section

Use markdown formatting. Be direct and professional. Keep it scannable."""

        response = await self.llm.ainvoke(prompt)

        # Parse response
        title, emoji = self._extract_title(response.content)
        sections = self._parse_sections(response.content)

        return CraftedMessage(
            title=title,
            emoji=emoji,
            body=response.content,
            sections=sections
        )
```

**Cost:** ~$0.0003 per call

---

### Agent 3: Action Recommendation

**Purpose:** Provide specific, actionable recommendations.

**Implementation:**
```python
class ActionRecommendationAgent:
    """Generate action recommendations based on threat"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

        # Embedded SOPs (no external database needed)
        self.sops = {
            "bird": {
                "large": ["Reduce altitude by 50 feet", "Maintain current speed"],
                "medium": ["Monitor closely", "Prepare for evasive action"],
                "small": ["Continue monitoring", "No immediate action required"]
            },
            "drone": {
                "large": ["Alert ATC immediately", "Reduce speed by 20%"],
                "medium": ["Monitor closely", "Report to ATC"],
                "small": ["Continue monitoring", "Log detection"]
            },
            # Similar for balloon, kite
        }

    async def recommend_actions(
        self,
        detection: Detection,
        context: EnrichedContext
    ) -> ActionRecommendation:

        # Get baseline SOPs
        baseline_actions = self.sops.get(
            detection.class_name, {}
        ).get(context.estimated_size, [])

        prompt = f"""You are an aviation safety advisor.

Situation:
- Hazard: {detection.class_name} ({context.estimated_size})
- Confidence: {detection.confidence:.0%}
- Position: {context.screen_position}

Baseline SOPs:
{chr(10).join(f"• {action}" for action in baseline_actions)}

Provide specific actions in 3 categories:
1. IMMEDIATE: Actions to take now
2. MONITORING: What to watch
3. CONTINGENCY: If situation worsens

Be specific and actionable. Use pilot terminology."""

        response = await self.llm.ainvoke(prompt)

        # Parse into categories
        immediate, monitoring, contingency = self._parse_actions(response.content)

        return ActionRecommendation(
            immediate_actions=immediate,
            monitoring_actions=monitoring,
            contingency_actions=contingency
        )
```

**Cost:** ~$0.0002 per call

---

### Agent 4: Priority Scoring

**Purpose:** Assign severity level and justify it.

**Implementation:**
```python
class PriorityAgent:
    """Determine alert priority level"""

    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    async def score_priority(
        self,
        detection: Detection,
        context: EnrichedContext
    ) -> PriorityScore:

        prompt = f"""Assess threat priority for aviation safety.

Detection:
- Object: {detection.class_name}
- Size: {context.estimated_size}
- Confidence: {detection.confidence:.0%}
- Position: {context.screen_position}

Priority Levels:
- RED (Critical): Immediate collision risk, requires instant action
- ORANGE (High): Significant risk, prompt action needed
- YELLOW (Medium): Moderate risk, heightened awareness required
- GREEN (Low): Minimal risk, standard monitoring

Assign priority level (RED/ORANGE/YELLOW/GREEN), a score (1-10), and brief reasoning (1-2 sentences)."""

        response = await self.llm.ainvoke(prompt)

        # Parse response
        level, score, reasoning = self._parse_priority(response.content)

        return PriorityScore(
            level=level.lower(),
            score=score,
            reasoning=reasoning
        )
```

**Cost:** ~$0.0001 per call

---

## Implementation Phases

### Phase 1: Setup & Infrastructure (Days 1-2)

**Tasks:**
1. Install dependencies
   ```bash
   cd apps/api
   pip install langgraph langchain-openai openai
   ```

2. Create project structure
   ```
   apps/api/app/
   ├── agents/
   │   ├── __init__.py
   │   ├── context_agent.py
   │   ├── message_agent.py
   │   ├── action_agent.py
   │   └── priority_agent.py
   ├── workflows/
   │   ├── __init__.py
   │   └── alert_workflow.py
   └── routers/
       └── alerts.py  (new)
   ```

3. Configure environment variables
   ```bash
   OPENAI_API_KEY=your_key_here
   ```

**Deliverable:** Project structure ready, dependencies installed

---

### Phase 2: Agent Implementation (Days 3-5)

**Day 3: Context & Message Agents**
- Implement `ContextEnrichmentAgent`
- Implement `MessageCraftingAgent`
- Write unit tests

**Day 4: Action & Priority Agents**
- Implement `ActionRecommendationAgent`
- Implement `PriorityAgent`
- Write unit tests

**Day 5: Testing & Refinement**
- Test with sample detections
- Refine prompts for quality
- Optimize performance

**Deliverable:** All 4 agents functional and tested

---

### Phase 3: LangGraph Workflow (Days 6-7)

**Day 6: Workflow Setup**
```python
from langgraph.graph import StateGraph, END

class AlertState(TypedDict):
    detection: Detection
    context: EnrichedContext
    message: CraftedMessage
    actions: ActionRecommendation
    priority: PriorityScore

workflow = StateGraph(AlertState)

# Add nodes
workflow.add_node("enrich_context", context_agent)
workflow.add_node("craft_message", message_agent)
workflow.add_node("recommend_actions", action_agent)
workflow.add_node("score_priority", priority_agent)

# Define edges
workflow.add_edge("enrich_context", "craft_message")
workflow.add_edge("craft_message", "recommend_actions")
workflow.add_edge("recommend_actions", "score_priority")
workflow.add_edge("score_priority", END)

# Set entry point
workflow.set_entry_point("enrich_context")

app = workflow.compile()
```

**Day 7: Integration Testing**
- Test full workflow
- Measure performance
- Optimize if needed

**Deliverable:** Working LangGraph workflow

---

### Phase 4: API Integration (Days 8-9)

**Day 8: FastAPI Endpoint**
```python
# apps/api/app/routers/alerts.py

@router.post("/api/v1/alerts/generate")
async def generate_alert(detection: Detection) -> NaturalLanguageAlert:
    """Generate natural language alert from detection"""

    # Run workflow
    result = await alert_workflow.ainvoke({
        "detection": detection
    })

    # Create alert object
    alert = NaturalLanguageAlert(
        alert_id=str(uuid4()),
        detection=detection,
        message=result["message"],
        actions=result["actions"],
        priority=result["priority"],
        generated_at=datetime.utcnow()
    )

    return alert
```

**Day 9: Testing**
- Test API endpoint
- Test error handling
- Load testing

**Deliverable:** API endpoint ready

---

### Phase 5: Frontend Integration (Days 10-12)

**Day 10: Alert Component**
```typescript
// apps/web/components/alerts/nl-alert-card.tsx

interface NLAlertCardProps {
  alert: NaturalLanguageAlert;
}

export function NLAlertCard({ alert }: NLAlertCardProps) {
  const priorityColors = {
    red: 'bg-red-500',
    orange: 'bg-orange-500',
    yellow: 'bg-yellow-500',
    green: 'bg-green-500'
  };

  return (
    <Card className={`border-l-4 ${priorityColors[alert.priority.level]}`}>
      <CardHeader>
        <CardTitle>
          {alert.message.emoji} {alert.message.title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Markdown>{alert.message.body}</Markdown>

        <Separator className="my-4" />

        <div className="space-y-2">
          <h4 className="font-semibold">Recommended Actions:</h4>
          <ul className="list-disc pl-5">
            {alert.actions.immediate_actions.map((action, i) => (
              <li key={i}>{action}</li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  );
}
```

**Day 11: Integration with Detection Flow**
```typescript
// apps/web/lib/hooks/use-detections.ts

async function processDetection(detection: Detection) {
  // Call alert generation API
  const alert = await fetch('/api/v1/alerts/generate', {
    method: 'POST',
    body: JSON.stringify(detection)
  }).then(r => r.json());

  // Display alert
  showAlert(alert);
}
```

**Day 12: Testing & Polish**
- Test UI rendering
- Test real-time updates
- Polish styling

**Deliverable:** Complete frontend integration

---

### Phase 6: Testing & Documentation (Days 13-14)

**Day 13: End-to-End Testing**
- Test complete flow: detection → alert → display
- Test edge cases
- Performance testing

**Day 14: Documentation**
- API documentation
- Component documentation
- User guide

**Deliverable:** Production-ready system

---

## Cost Analysis

### Per-Alert Cost Breakdown

| Agent | Est. Tokens | Cost/Alert |
|-------|-------------|------------|
| Context Agent | 0 (rule-based) | $0 |
| Message Agent | 700 | $0.0003 |
| Action Agent | 500 | $0.0002 |
| Priority Agent | 300 | $0.0001 |
| **Total** | **1,500** | **$0.0006** |

**Monthly Estimate (10,000 alerts):** ~$6

---

## Success Metrics

### Technical Metrics
- **Latency:** < 2 seconds per alert (target: < 1s)
- **Success Rate:** > 99%
- **Cost:** < $0.001 per alert

### Quality Metrics
- **Message Clarity:** Operator can understand in < 5 seconds
- **Action Relevance:** Actions are appropriate to threat
- **Priority Accuracy:** Priority matches human expert judgment

---

## Testing Strategy

### Unit Tests
```python
def test_context_agent():
    detection = Detection(...)
    context = context_agent.enrich(detection)
    assert context.estimated_size in ["small", "medium", "large"]
    assert context.screen_position is not None

async def test_message_agent():
    detection = Detection(...)
    context = EnrichedContext(...)
    message = await message_agent.craft_message(detection, context)
    assert message.title is not None
    assert message.emoji is not None
    assert len(message.body) > 0
```

### Integration Tests
```python
async def test_full_workflow():
    detection = create_test_detection()
    result = await alert_workflow.ainvoke({"detection": detection})

    assert "context" in result
    assert "message" in result
    assert "actions" in result
    assert "priority" in result

    alert = NaturalLanguageAlert(**result)
    assert alert.priority.level in ["green", "yellow", "orange", "red"]
```

### Manual Testing
- Test with real detection samples
- Review alert quality
- Test different scenarios (bird sizes, positions, etc.)

---

## Deployment

### Environment Variables
```bash
# .env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
ALERT_GENERATION_TIMEOUT=5
```

### Deployment Steps
1. Deploy backend changes to FastAPI
2. Update frontend with new components
3. Monitor initial alerts
4. Gather feedback
5. Iterate on prompts

---

## Future Enhancements (Optional)

### Phase 2 (If Needed)
- Add historical context (query past detections)
- Add environmental data (weather, time of day)
- Add feedback loop for continuous improvement
- Add alert history and analytics
- Add custom SOP integration
- Add multi-language support

### Advanced Features
- Voice alerts
- Alert aggregation (multiple detections)
- Predictive alerts (trajectory-based)
- Integration with traffic management systems

---

## Appendix

### Sample Alert Output

```
🔴 CRITICAL ALERT

🦅 Large Bird Detection
Detected at 41.1 seconds | Upper-right quadrant | 87% confidence

📊 Threat Assessment:
• Size: Large (estimated 2-3 kg based on detection area)
• Position: Upper-right quadrant (potential flight path intersection)
• Confidence Level: High (87%)

⚠️ RECOMMENDED ACTIONS:

IMMEDIATE:
• Reduce altitude by 50 feet
• Maintain current speed
• Alert ATC of bird strike risk

MONITORING:
• Monitor right-side camera for visual confirmation
• Watch for flock behavior
• Track object movement

CONTINGENCY:
• If bird remains in path: execute 15° course deviation to port
• If multiple birds detected: request altitude change clearance
• Be prepared for emergency landing if strike occurs

Priority: HIGH (8/10)
Reasoning: Large bird at high confidence in potential collision path requires immediate altitude adjustment to ensure safety.

Alert ID: a7f3c9d2-4e8b-11ef-8e9a-0242ac120002
Generated: 2025-11-01 14:32:18 UTC
```

---

## Getting Started

### Quick Start Commands

```bash
# 1. Install dependencies
cd apps/api
pip install langgraph langchain-openai openai

# 2. Set environment variables
export OPENAI_API_KEY=your_key_here

# 3. Run tests
pytest tests/agents/

# 4. Start API server
uvicorn app.main:app --reload

# 5. Test alert generation
curl -X POST http://localhost:8000/api/v1/alerts/generate \
  -H "Content-Type: application/json" \
  -d '{"class_name": "bird", "confidence": 0.87, ...}'
```

---

## Questions & Decisions

### Key Simplifications Made
1. **No historical database queries** - All context from current detection only
2. **No external weather APIs** - Environmental context removed
3. **No feedback loop agent** - No learning/improvement mechanism (for now)
4. **Embedded SOPs** - No external SOP database, hardcoded in agents
5. **Synchronous workflow** - No async feedback collection

### Trade-offs
- **Simpler implementation** ✅ vs **Less contextual richness** ❌
- **Lower latency** ✅ vs **Less accurate threat assessment** ❌
- **Easier to maintain** ✅ vs **No continuous improvement** ❌

### When to Add Complexity
Add historical context if:
- Operators report alerts lack important pattern information
- Certain locations consistently have hazards
- Temporal patterns are critical for safety

Add feedback loop if:
- Alert quality needs improvement
- False positive rate is high
- Operators request customization

---

**End of Simplified Implementation Plan**
