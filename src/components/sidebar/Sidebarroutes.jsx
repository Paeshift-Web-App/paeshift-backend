import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHome, faUser, faGear, faUserGroup, faTableCells, faSuitcase  } from "@fortawesome/free-solid-svg-icons";
import { faProductHunt } from "@fortawesome/free-brands-svg-icons";

let id = 0;

export const sidebarRoutes = [
	{
		id: id++,
		to: '../dashboard',
		title: 'Dashboard',
		icon: <FontAwesomeIcon className='me-2' icon={faTableCells} />,
	},
	{
		id: id++,
		to: '../home',
		title: 'Home',
		icon: <FontAwesomeIcon className='me-2' icon={faTableCells} />,
	},
	{
		id: id++,
		to: '../jobs',
		title: 'Jobs',
		icon: <FontAwesomeIcon className='me-2' icon={faSuitcase} />,
		role: "admin"
	},
	{
		id: id++,
		to: '../settings',
		title: 'Settings',
		icon: <FontAwesomeIcon className='me-2' icon={faGear} />,
		role: "admin"
	},
	
]
export const applicantSidebarRoutes = [
	{
		id: id++,
		to: '../dashboard',
		title: 'Dashboard',
		icon: <FontAwesomeIcon className='me-2' icon={faTableCells} />,
	},
	{
		id: id++,
		to: '../home',
		title: 'Home',
		icon: <FontAwesomeIcon className='me-2' icon={faTableCells} />,
	},
	{
		id: id++,
		to: '../jobs',
		title: 'Jobs',
		icon: <FontAwesomeIcon className='me-2' icon={faSuitcase} />,
		role: "admin"
	},
	{
		id: id++,
		to: '../settings',
		title: 'Settings',
		icon: <FontAwesomeIcon className='me-2' icon={faGear} />,
		role: "admin"
	},
	
]