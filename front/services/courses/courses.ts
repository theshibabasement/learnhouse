import { getAPIUrl } from "@services/config/config";
import { RequestBody, RequestBodyForm, errorHandling } from "@services/utils/ts/requests";

/*
 This file includes only POST, PUT, DELETE requests
 GET requests are called from the frontend using SWR (https://swr.vercel.app/)
*/

export async function getOrgCourses(org_id: number) {
  const result: any = await fetch(`${getAPIUrl()}courses/org_slug/${org_id}/page/1/limit/10`, RequestBody("GET", null));
  const res = await errorHandling(result);
  
  return res;
}

export async function getCourse(course_id: string) {
  const result: any = await fetch(`${getAPIUrl()}courses/${course_id}`, RequestBody("GET", null));
  const res = await errorHandling(result);
  return res;
}

export async function createNewCourse(org_id: string, course_body: any, thumbnail: any) {
  // Send file thumbnail as form data
  const formData = new FormData();
  formData.append("thumbnail", thumbnail);
  formData.append("name", course_body.name);
  formData.append("description", course_body.description);
  formData.append("mini_description", "course_body.mini_description");
  formData.append("public", "true");

  const result = await fetch(`${getAPIUrl()}courses/?org_id=${org_id}`, RequestBodyForm("POST", formData));
  const res = await errorHandling(result);
  return res;
}

export async function deleteCourseFromBackend(course_id: any) {
  const result: any = await fetch(`${getAPIUrl()}courses/${course_id}`, RequestBody("DELETE", null));
  const res = await errorHandling(result);
  return res;
}
