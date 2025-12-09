# Phase 2: API & UI Design

**Document:** PHASE2_API_UI.md  
**Part of:** Phase 2 Solution Architecture (Author-Level Faculty Statistics)  
**Prerequisites:** PHASE2_STATISTICS.md

---

## Table of Contents

1. API Endpoints
2. Request/Response Examples
3. UI Components
4. Workflow Integration
5. Error Handling

---

## 1. API Endpoints

### 1.1 Author Faculty Management

#### **GET /v2/authors/{author_uuid}/faculty**

Get faculty assignment for an author.

**Request:**
```http
GET /v2/authors/abc-123/faculty HTTP/1.1
Host: data.4tu.nl
Accept: application/json
```

**Response (200 OK):**
```json
{
  "author_uuid": "abc-123",
  "full_name": "Dr. Jane Smith",
  "faculty": {
    "faculty_id": 285860001,
    "faculty_name": "Faculty of Aerospace Engineering",
    "faculty_short_name": "Aerospace",
    "faculty_code": "AE"
  },
  "assignment": {
    "confidence": 1.0,
    "source": "account",
    "assigned_date": "2025-12-09T10:30:00Z",
    "assigned_by": "system"
  },
  "linked_account": {
    "account_uuid": "def-456",
    "email": "j.smith@tudelft.nl"
  }
}
```

**Response (404 Not Found - No Faculty):**
```json
{
  "error": "No faculty assignment found",
  "author_uuid": "abc-123",
  "full_name": "Hebly, Scott J.",
  "institution_id": 28586,
  "has_account": false,
  "suggested_action": "Review Organizations field to assign faculty"
}
```

---

#### **PATCH /v2/authors/{author_uuid}/faculty**

Assign or update faculty for an author.

**Request:**
```http
PATCH /v2/authors/abc-123/faculty HTTP/1.1
Host: data.4tu.nl
Content-Type: application/json
Authorization: Bearer <session_token>

{
  "faculty_id": 285860005,
  "confidence": 1.0,
  "source": "manual_review",
  "notes": "Verified via ORCID profile showing EEMCS affiliation 2020-present"
}
```

**Response (200 OK):**
```json
{
  "message": "Faculty assignment updated successfully",
  "author_uuid": "abc-123",
  "faculty_id": 285860005,
  "previous_faculty_id": null,
  "updated_at": "2025-12-09T14:20:00Z"
}
```

**Validation Errors (400 Bad Request):**
```json
{
  "error": "Invalid faculty assignment",
  "details": [
    {
      "field": "faculty_id",
      "message": "Faculty 285860005 does not belong to author's institution (28586)"
    }
  ]
}
```

---

### 1.2 Faculty-Authored Statistics

#### **GET /v2/statistics/faculties/authored**

Get dataset counts by author faculty (Phase 2).

**Request:**
```http
GET /v2/statistics/faculties/authored?institution_id=28586&min_confidence=0.8 HTTP/1.1
Host: data.4tu.nl
Accept: application/json
```

**Response (200 OK):**
```json
{
  "institution_id": 28586,
  "institution_name": "TU Delft",
  "min_confidence": 0.8,
  "statistics": [
    {
      "faculty_id": 285860001,
      "faculty_name": "Faculty of Aerospace Engineering",
      "faculty_short_name": "Aerospace",
      "dataset_count": 152,
      "author_count": 87,
      "registered_authors": 23,
      "unregistered_authors": 64,
      "avg_confidence": 0.89
    },
    {
      "faculty_id": 285860005,
      "faculty_name": "Faculty of EEMCS",
      "faculty_short_name": "EEMCS",
      "dataset_count": 134,
      "author_count": 102,
      "registered_authors": 31,
      "unregistered_authors": 71,
      "avg_confidence": 0.87
    },
    ...
  ],
  "metadata": {
    "total_datasets": 580,
    "total_authors": 950,
    "generated_at": "2025-12-09T15:00:00Z",
    "cache_age": 120
  }
}
```

**CSV Export:**
```http
GET /v2/statistics/faculties/authored?format=csv HTTP/1.1
```

```csv
faculty_id,faculty_name,dataset_count,author_count,avg_confidence
285860001,"Faculty of Aerospace Engineering",152,87,0.89
285860005,"Faculty of EEMCS",134,102,0.87
...
```

---

#### **GET /v2/statistics/faculties/{faculty_id}/datasets**

Get datasets authored by a specific faculty.

**Request:**
```http
GET /v2/statistics/faculties/285860001/datasets?limit=20&offset=0 HTTP/1.1
Host: data.4tu.nl
Accept: application/json
```

**Response (200 OK):**
```json
{
  "faculty_id": 285860001,
  "faculty_name": "Faculty of Aerospace Engineering",
  "total_count": 152,
  "limit": 20,
  "offset": 0,
  "datasets": [
    {
      "uuid": "abc-123",
      "title": "Aviation NOx Emissions Modeling",
      "published_date": "2024-03-15",
      "doi": "10.4121/abc-123",
      "authors": [
        {
          "full_name": "Dr. Jane Smith",
          "faculty_id": 285860001,
          "is_registered": true
        },
        {
          "full_name": "Hebly, Scott J.",
          "faculty_id": 285860001,
          "is_registered": false
        },
        {
          "full_name": "Dr. Johnson",
          "faculty_id": 285860005,
          "is_registered": true
        }
      ],
      "collaboration": {
        "is_multi_faculty": true,
        "other_faculties": ["Faculty of EEMCS"],
        "is_external": false
      }
    },
    ...
  ]
}
```

---

### 1.3 Collaboration Metrics

#### **GET /v2/statistics/collaborations**

Get faculty collaboration matrix.

**Request:**
```http
GET /v2/statistics/collaborations?institution_id=28586 HTTP/1.1
Host: data.4tu.nl
Accept: application/json
```

**Response (200 OK):**
```json
{
  "institution_id": 28586,
  "institution_name": "TU Delft",
  "collaborations": [
    {
      "faculty1": {
        "faculty_id": 285860001,
        "name": "Aerospace"
      },
      "faculty2": {
        "faculty_id": 285860005,
        "name": "EEMCS"
      },
      "collaboration_count": 23,
      "example_datasets": ["abc-123", "def-456", "ghi-789"]
    },
    {
      "faculty1": {
        "faculty_id": 285860001,
        "name": "Aerospace"
      },
      "faculty2": {
        "faculty_id": 285860007,
        "name": "Mechanical"
      },
      "collaboration_count": 18,
      "example_datasets": ["jkl-012", "mno-345"]
    },
    ...
  ],
  "network_graph": {
    "nodes": [
      {"id": 285860001, "name": "Aerospace", "datasets": 152},
      {"id": 285860005, "name": "EEMCS", "datasets": 134},
      ...
    ],
    "edges": [
      {"source": 285860001, "target": 285860005, "weight": 23},
      {"source": 285860001, "target": 285860007, "weight": 18},
      ...
    ]
  }
}
```

---

### 1.4 Author Contributions

#### **GET /v2/authors?faculty_id={faculty_id}**

Get authors for a faculty, sorted by contribution.

**Request:**
```http
GET /v2/authors?faculty_id=285860001&sort=dataset_count&limit=50 HTTP/1.1
Host: data.4tu.nl
Accept: application/json
```

**Response (200 OK):**
```json
{
  "faculty_id": 285860001,
  "faculty_name": "Faculty of Aerospace Engineering",
  "total_authors": 87,
  "authors": [
    {
      "author_uuid": "abc-123",
      "full_name": "Dr. Jane Smith",
      "orcid_id": "0000-0003-1234-5678",
      "is_registered": true,
      "account_uuid": "def-456",
      "dataset_count": 12,
      "faculty_confidence": 1.0,
      "faculty_source": "account"
    },
    {
      "author_uuid": "ghi-789",
      "full_name": "Hebly, Scott J.",
      "orcid_id": null,
      "is_registered": false,
      "account_uuid": null,
      "dataset_count": 3,
      "faculty_confidence": 0.85,
      "faculty_source": "organizations_auto"
    },
    ...
  ]
}
```

---

## 2. Request/Response Examples

### 2.1 Python Route Handler Example

**File:** `src/djehuty/web/wsgi.py`

```python
@app.route("/v2/statistics/faculties/authored", methods=["GET"])
def api_v2_statistics_faculty_authored():
    """Get dataset counts by author faculty (Phase 2)."""
    
    institution_id = request.args.get('institution_id', type=int)
    min_confidence = request.args.get('min_confidence', 0.0, type=float)
    format_type = request.args.get('format', 'json')
    
    # Validate inputs
    if min_confidence < 0.0 or min_confidence > 1.0:
        return jsonify({
            'error': 'Invalid min_confidence',
            'message': 'Must be between 0.0 and 1.0'
        }), 400
    
    # Get statistics (cached)
    cache_key = f"faculty_authored_{institution_id}_{min_confidence}"
    stats = self.db.cache.get(cache_key)
    
    if stats is None:
        stats = self.db.faculty_authored_statistics(
            institution_id=institution_id,
            min_confidence=min_confidence
        )
        self.db.cache.set(cache_key, stats, ttl=21600)  # 6 hours
    
    # Format response
    if format_type == 'csv':
        return generate_csv_response(stats)
    else:
        return jsonify({
            'institution_id': institution_id,
            'min_confidence': min_confidence,
            'statistics': stats,
            'metadata': {
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'cache_age': self.db.cache.age(cache_key)
            }
        })

@app.route("/v2/authors/<author_uuid>/faculty", methods=["PATCH"])
@require_authentication
def api_v2_update_author_faculty(author_uuid):
    """Update author faculty assignment."""
    
    # Parse request body
    data = request.get_json()
    faculty_id = data.get('faculty_id')
    confidence = data.get('confidence', 1.0)
    source = data.get('source', 'manual')
    notes = data.get('notes', '')
    
    # Validate faculty_id
    if not self.db.faculty_exists(faculty_id):
        return jsonify({
            'error': 'Invalid faculty_id',
            'message': f'Faculty {faculty_id} does not exist'
        }), 400
    
    # Get author details
    author = self.db.author(author_uuid)
    if not author:
        return jsonify({'error': 'Author not found'}), 404
    
    # Validate institution match
    faculty_institution = self.db.get_faculty_institution(faculty_id)
    if author.get('institution_id') != faculty_institution:
        return jsonify({
            'error': 'Institution mismatch',
            'message': f'Author institution {author["institution_id"]} does not match faculty institution {faculty_institution}'
        }), 400
    
    # Update faculty
    success = self.db.update_author_faculty(
        author_uuid=author_uuid,
        faculty_id=faculty_id,
        confidence=confidence,
        source=source,
        assigned_by=self.account_uuid,
        notes=notes
    )
    
    if success:
        # Invalidate caches
        self.db.invalidate_faculty_caches(faculty_id)
        
        return jsonify({
            'message': 'Faculty assignment updated',
            'author_uuid': author_uuid,
            'faculty_id': faculty_id
        })
    else:
        return jsonify({'error': 'Update failed'}), 500
```

---

## 3. UI Components

### 3.1 Author Faculty Badge (Author Profile)

**Component:** Display author's faculty affiliation on public profile page.

**Location:** `/authors/{author_uuid}` page

**HTML:**
```html
<div class="author-profile">
  <h1>{{ author.full_name }}</h1>
  
  {% if author.faculty %}
  <div class="faculty-badge">
    <i class="icon-building"></i>
    <span class="faculty-name">{{ author.faculty.name }}</span>
    {% if author.faculty.confidence < 1.0 %}
    <span class="confidence-indicator" title="Auto-assigned with {{ author.faculty.confidence * 100 }}% confidence">
      <i class="icon-info"></i>
    </span>
    {% endif %}
  </div>
  {% endif %}
  
  {% if author.institution %}
  <div class="institution-badge">
    <span>{{ author.institution.name }}</span>
  </div>
  {% endif %}
</div>
```

**CSS:**
```css
.faculty-badge {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  background: #0066CC;
  color: white;
  border-radius: 20px;
  font-size: 14px;
  margin: 8px 0;
}

.confidence-indicator {
  margin-left: 8px;
  color: #FFC107;
  cursor: help;
}
```

---

### 3.2 Multi-Faculty Collaboration Dashboard

**Component:** Visual dashboard showing faculty collaboration network.

**Location:** `/statistics/collaborations` page

**HTML:**
```html
<div class="collaboration-dashboard">
  <h2>Faculty Collaboration Network</h2>
  
  <!-- Filters -->
  <div class="filters">
    <label>
      Institution:
      <select id="institution-filter">
        <option value="28586" selected>TU Delft</option>
        <option value="all">All 4TU institutions</option>
      </select>
    </label>
    <label>
      Minimum Collaborations:
      <input type="number" id="min-collabs" value="5" min="1">
    </label>
  </div>
  
  <!-- Network Graph (D3.js) -->
  <div id="collaboration-network" style="width: 100%; height: 600px;"></div>
  
  <!-- Collaboration Table -->
  <table class="collaboration-table">
    <thead>
      <tr>
        <th>Faculty 1</th>
        <th>Faculty 2</th>
        <th>Collaborations</th>
        <th>Example Datasets</th>
      </tr>
    </thead>
    <tbody id="collaboration-data">
      <!-- Populated via JavaScript -->
    </tbody>
  </table>
</div>
```

**JavaScript (D3.js Network Graph):**
```javascript
function renderCollaborationNetwork() {
  fetch('/v2/statistics/collaborations?institution_id=28586')
    .then(response => response.json())
    .then(data => {
      const width = 900;
      const height = 600;
      
      const svg = d3.select('#collaboration-network')
        .append('svg')
        .attr('width', width)
        .attr('height', height);
      
      // Force simulation
      const simulation = d3.forceSimulation(data.network_graph.nodes)
        .force('link', d3.forceLink(data.network_graph.edges)
                         .id(d => d.id)
                         .distance(d => 100 / Math.sqrt(d.weight)))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2));
      
      // Draw edges
      const link = svg.append('g')
        .selectAll('line')
        .data(data.network_graph.edges)
        .enter().append('line')
        .attr('stroke', '#999')
        .attr('stroke-width', d => Math.sqrt(d.weight));
      
      // Draw nodes
      const node = svg.append('g')
        .selectAll('circle')
        .data(data.network_graph.nodes)
        .enter().append('circle')
        .attr('r', d => Math.sqrt(d.datasets) * 2)
        .attr('fill', d => facultyColor(d.id))
        .call(drag(simulation));
      
      // Node labels
      const label = svg.append('g')
        .selectAll('text')
        .data(data.network_graph.nodes)
        .enter().append('text')
        .text(d => d.name)
        .attr('font-size', 12)
        .attr('dx', 15)
        .attr('dy', 4);
      
      // Update positions on tick
      simulation.on('tick', () => {
        link
          .attr('x1', d => d.source.x)
          .attr('y1', d => d.source.y)
          .attr('x2', d => d.target.x)
          .attr('y2', d => d.target.y);
        
        node
          .attr('cx', d => d.x)
          .attr('cy', d => d.y);
        
        label
          .attr('x', d => d.x)
          .attr('y', d => d.y);
      });
      
      // Populate table
      populateCollaborationTable(data.collaborations);
    });
}

function populateCollaborationTable(collaborations) {
  const tbody = document.getElementById('collaboration-data');
  tbody.innerHTML = '';
  
  collaborations.forEach(collab => {
    const row = tbody.insertRow();
    row.innerHTML = `
      <td>${collab.faculty1.name}</td>
      <td>${collab.faculty2.name}</td>
      <td>${collab.collaboration_count}</td>
      <td>
        ${collab.example_datasets.slice(0, 3).map(uuid => 
          `<a href="/datasets/${uuid}" target="_blank">${uuid.slice(0, 8)}...</a>`
        ).join(', ')}
      </td>
    `;
  });
}
```

---

### 3.3 Faculty Statistics Comparison (Phase 1 vs Phase 2)

**Component:** Side-by-side comparison of deposited vs authored statistics.

**Location:** `/statistics/faculties` page

**HTML:**
```html
<div class="faculty-stats-comparison">
  <h2>Faculty Research Profile</h2>
  
  <div class="stat-toggle">
    <button class="toggle-btn active" data-view="authored">
      Authored Datasets (Phase 2)
    </button>
    <button class="toggle-btn" data-view="deposited">
      Deposited Datasets (Phase 1)
    </button>
    <button class="toggle-btn" data-view="comparison">
      Comparison
    </button>
  </div>
  
  <div id="stats-view-authored" class="stats-view active">
    <canvas id="authored-chart"></canvas>
    <p class="explanation">
      Counts datasets where faculty researchers are listed as authors.
      Multi-faculty datasets counted for each contributing faculty.
    </p>
  </div>
  
  <div id="stats-view-deposited" class="stats-view hidden">
    <canvas id="deposited-chart"></canvas>
    <p class="explanation">
      Counts datasets deposited by faculty members.
      Each dataset counted once for the depositor's faculty.
    </p>
  </div>
  
  <div id="stats-view-comparison" class="stats-view hidden">
    <canvas id="comparison-chart"></canvas>
    <p class="explanation">
      Blue: Deposited (management) | Orange: Authored (contribution)
    </p>
  </div>
</div>
```

**JavaScript (Chart.js):**
```javascript
fetch('/v2/statistics/faculties/combined')
  .then(response => response.json())
  .then(data => {
    const labels = data.map(f => f.faculty_short_name);
    const depositedData = data.map(f => f.deposited_count);
    const authoredData = data.map(f => f.authored_count);
    
    // Authored chart
    new Chart(document.getElementById('authored-chart'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Authored Datasets',
          data: authoredData,
          backgroundColor: '#FF9800'
        }]
      },
      options: {
        scales: {
          y: { beginAtZero: true }
        }
      }
    });
    
    // Deposited chart
    new Chart(document.getElementById('deposited-chart'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [{
          label: 'Deposited Datasets',
          data: depositedData,
          backgroundColor: '#2196F3'
        }]
      }
    });
    
    // Comparison chart
    new Chart(document.getElementById('comparison-chart'), {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Deposited',
            data: depositedData,
            backgroundColor: '#2196F3'
          },
          {
            label: 'Authored',
            data: authoredData,
            backgroundColor: '#FF9800'
          }
        ]
      }
    });
  });
```

---

## 4. Workflow Integration

### 4.1 Dataset Submission with Author Faculty

**Scenario:** User submits dataset with multiple co-authors.

**Workflow:**

1. **Step 1:** User fills dataset metadata form
2. **Step 2:** User adds authors (registered or unregistered)
3. **Step 3:** For each author:
   - If registered (has account): Faculty auto-populated from account
   - If unregistered: Faculty dropdown shown (optional)
4. **Step 4:** System validates faculty assignments match institution
5. **Step 5:** Dataset published with author faculty data

**UI Mock:**

```html
<form id="dataset-authors-form">
  <h3>Authors</h3>
  
  <!-- Author 1 (Registered) -->
  <div class="author-entry registered">
    <input type="text" value="Dr. Jane Smith" readonly>
    <span class="faculty-badge">Aerospace</span>
    <span class="info">From account profile</span>
  </div>
  
  <!-- Author 2 (Unregistered) -->
  <div class="author-entry unregistered">
    <input type="text" name="author_name" placeholder="Full name" required>
    <select name="author_faculty" required>
      <option value="">Select faculty...</option>
      <option value="285860001">Faculty of Aerospace Engineering</option>
      <option value="285860002">Faculty of Architecture</option>
      ...
    </select>
    <span class="optional-badge">Optional</span>
  </div>
  
  <button type="button" id="add-author">+ Add Author</button>
</form>
```

---

## 5. Error Handling

### 5.1 Common Errors

**Error 1: Faculty-Institution Mismatch**
```json
{
  "error": "faculty_institution_mismatch",
  "message": "Faculty 285860001 (TU Delft) cannot be assigned to author with institution_id 28587 (UT)",
  "author_uuid": "abc-123",
  "author_institution": 28587,
  "faculty_institution": 28586
}
```

**Error 2: Low Confidence Warning**
```json
{
  "warning": "low_confidence_assignment",
  "message": "Faculty assignment has low confidence (0.45). Consider manual review.",
  "author_uuid": "def-456",
  "faculty_id": 285860003,
  "confidence": 0.45,
  "source": "organizations_auto",
  "suggested_action": "manual_review"
}
```

**Error 3: Missing Prerequisite (Phase 1 not complete)**
```json
{
  "error": "prerequisite_not_met",
  "message": "Phase 1 migration not complete. Account faculty_id missing.",
  "account_uuid": "ghi-789",
  "required_action": "Complete Phase 1: Assign faculty_id to account first"
}
```

---

## Summary

Phase 2 API adds **6 new endpoints**:
1. GET/PATCH author faculty assignment
2. GET faculty-authored statistics
3. GET datasets by faculty (authored)
4. GET collaboration matrix
5. GET authors by faculty
6. GET combined Phase 1/2 statistics

**UI Components:**
1. Author faculty badge on profiles
2. Multi-faculty collaboration network (D3.js)
3. Phase 1 vs Phase 2 statistics comparison (Chart.js)

**Integration:** Author faculty selection during dataset submission.

---

**Next Document:** PHASE2_IMPLEMENTATION.md (Timeline, testing, deployment)

**Navigation:**
- Previous: PHASE2_STATISTICS.md
- Current: PHASE2_API_UI.md
- Next: PHASE2_IMPLEMENTATION.md
