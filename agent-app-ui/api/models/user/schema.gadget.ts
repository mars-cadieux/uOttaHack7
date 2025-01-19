import type { GadgetModel } from "gadget-server";

// This file describes the schema for the "user" model, go to https://agent-app-ui.gadget.app/edit to view/edit your model in Gadget
// For more information on how to update this file http://docs.gadget.dev

export const schema: GadgetModel = {
  type: "gadget/model-schema/v1",
  storageKey: "mosYOqDIG4p7",
  fields: {
    email: {
      type: "email",
      validations: { required: true, unique: true },
      storageKey: "T0S-kLazXWQB",
    },
    emailVerificationToken: {
      type: "string",
      storageKey: "uLEGIFGlJ1O-",
    },
    emailVerificationTokenExpiration: {
      type: "dateTime",
      includeTime: true,
      storageKey: "7vd7SMNmBheW",
    },
    emailVerified: {
      type: "boolean",
      default: false,
      storageKey: "FWV865y26DUp",
    },
    firstName: { type: "string", storageKey: "Xf59ZrrNqzTz" },
    googleImageUrl: { type: "url", storageKey: "0IeJHJ_i_3Ch" },
    googleProfileId: { type: "string", storageKey: "Wy4o-fCO8Oup" },
    lastName: { type: "string", storageKey: "7IScK8hUfMKp" },
    lastSignedIn: {
      type: "dateTime",
      includeTime: true,
      storageKey: "b5geVmwzdOCe",
    },
    password: {
      type: "password",
      validations: { strongPassword: true },
      storageKey: "MkGo7qT6mmk6",
    },
    profilePicture: {
      type: "file",
      allowPublicAccess: true,
      storageKey: "0kVEr1D3xMhl",
    },
    resetPasswordToken: {
      type: "string",
      storageKey: "zAZWQVL_sfmd",
    },
    resetPasswordTokenExpiration: {
      type: "dateTime",
      includeTime: true,
      storageKey: "_m1ffJwDcmts",
    },
    roles: {
      type: "roleList",
      default: ["unauthenticated"],
      storageKey: "w1ePcjVFBXb3",
    },
  },
};
