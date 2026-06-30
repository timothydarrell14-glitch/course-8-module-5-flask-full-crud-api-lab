from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route('/')
def home():
    return "Welcome to the Home Page", 200

app.route('/events', methods=["GET"])
def get_events():
    all_events = []
    for e in events:
        all_events.append(e.__dict__)
    return jsonify(all_events)

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    new_id = max([e.id for e in events]) + 1 if events else 1
    new_event = Event(id=new_id, title=data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    event = next((e for e in events if event_id == id), None)
    if not event:
        return ("Event not found"), 404
    if "title" in data:
        event.title = data["title"]
    return jsonify(event.to_dict()), 201


@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events
    event = next((e for e in events if event_id == id), None)
    if not event:
        return ("Event not found"), 404
    events = [e for e in events if event_id != id]
    return ("Event deleted"), 204

if __name__ == "__main__":
    app.run(debug=True)
