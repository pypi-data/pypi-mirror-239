import datetime, csv, click, logging
from urllib.parse import urlparse
from xml.etree.ElementTree import Element
from ics import Calendar, Event, Attendee
from pyade import ADEWebAPI, Config
from InquirerPy.inquirer import select as prompt_select


class BetterADEWebAPI(ADEWebAPI):
    """Extends ``ADEWebAPI``\ ."""

    # Fixes on the ADEWebAPI attributes.
    # Until the package ``pyade`` is beeing updated on pypi.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opt_params: dict[str, set[str]]  # type hint.
        self.opt_params["getActivities"].add("detail")
        # add detail field to getActivities API.

    @staticmethod
    def get_event_additional_info(event: Element, info_key: str) -> str:
        """Get additional information from an event.

        Args:
            event (Element): the XML element corresponding to the event.
            info_key (str): the key (XML resource element->category) to search.

        Returns:
            str: the information data or an empty string.
        """
        infos = event.findall(f"resources/resource[@category='{info_key}']")
        if len(infos) > 0:
            return infos[0].get("name")
        return ""

    def getEvents(self, **kwargs) -> list[dict[str, str]]:
        function, typ = "getEvents", "event"
        self._test_opt_params(kwargs, function)
        element = self._send_request(function, **kwargs)
        events = element.findall(typ)
        result = []

        for event in events:
            classroom = self.get_event_additional_info(event, "classroom")
            instructor = self.get_event_additional_info(event, "instructor")
            result.append(event.attrib | {"classroom": classroom, "instructor": instructor})

        return result


class SkipResourceException(Exception):
    ...


def determine_resource_search_parameters(cell_value: str) -> dict:
    """
    Args:
        cell_value (str): the value of the CSV cell.

    Raises:
        SkipResourceException: if we should skip the resource search for this cell.

    Returns:
        dict: the parameters to find the resource depending on the cell value.
    """
    groups = cell_value.split("_")
    if len(groups) < 5:
        raise SkipResourceException
    return {"name": f"{groups[2]}-{groups[3]}"}


@click.command()
@click.argument("csv_file", type=click.Path(exists=True), required=True)
@click.option("--url", "-u", type=click.STRING, help="The URL of the ADE API.", required=True)
@click.option("--login", "-l", type=click.STRING, help="The username used to connect to ADE.", default="")
@click.option("--password", "-p", type=click.STRING, help="The password used to connect to ADE.", default="")
@click.option(
    "--out",
    "-o",
    type=click.Path(exists=False),
    help="The output file to generate.",
    default="caladar.ics",
)
@click.option(
    "--col_index",
    "-col",
    type=click.INT,
    help="The index of the column used to find resources.",
    default=0,
)
@click.option("--debug", is_flag=True, help="Debug.")
def process_csv(csv_file: str, url: str, login: str, password: str, out: str, col_index: int, debug: bool):
    uri = urlparse(url)
    if not uri.scheme:
        url = "https://" + url
        uri = urlparse(url)
    if not url.endswith("/jsp/webapi"):
        url = f"{uri.scheme}://{uri.netloc}/jsp/webapi"
    if not out.endswith(".ics"):
        out += ".ics"
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    # Processing arguments.

    ade_api = BetterADEWebAPI(**Config.create(url=url, login=login, password=password))

    try:
        ade_api.connect()
    except Exception as e:
        logging.debug(e)
        click.echo("Connection failed.")
        exit(1)

    calendar = Calendar()
    activity_titles = {}
    create_datetime = lambda date, hour: datetime.datetime.strptime(date + hour, "%d/%m/%Y%H:%M")

    project_id = prompt_select(
        "Select an ADE project.",
        [{"name": project["name"], "value": project["id"]} for project in ade_api.getProjects(detail=4)],
    ).execute()

    ade_api.setProject(project_id)
    click.echo("Processing...")

    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # skip first line (column names).

        for row in csv_reader:
            try:
                resource_identifiers = [
                    resource["id"]
                    for resource in ade_api.getResources(
                        **determine_resource_search_parameters(row[col_index]), detail=4
                    )
                    if resource["isGroup"] == "true"
                ]
            except SkipResourceException:
                continue

            for event in ade_api.getEvents(resources=resource_identifiers, detail=8):
                if not (event_name := event["name"]) in set(activity_titles.keys()):
                    activity: dict = next(ade_api.getActivities(id=event["activityId"], detail=9))
                    activity_titles[event_name] = activity["code"] if "code" in set(activity.keys()) else ""

                calendar.events.add(
                    Event(
                        name=f"{event['name']} - {activity_titles[event_name]}",
                        begin=create_datetime(event["date"], event["startHour"]),
                        end=create_datetime(event["date"], event["endHour"]),
                        location=event["classroom"],
                        attendees=[Attendee(email="", common_name=event["instructor"])],
                        description=event["instructor"],
                    )
                )

    with open(out, "w") as f:
        f.writelines(calendar.serialize_iter())
    click.echo(out)


if __name__ == "__main__":
    process_csv()
